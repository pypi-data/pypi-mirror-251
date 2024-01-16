"""
Slightly modified code from https://github.com/djosix/Performance-RNN-PyTorch on MIT licence.
"""

import torch
import torch.nn as nn
from torch.distributions import Categorical, Gumbel

import numpy as np
from progress.bar import Bar

from coopertunes.hparams.PerformanceRNN import PerformanceRNNHParams


class PerformanceRNN(nn.Module):
    def __init__(self, hparams: PerformanceRNNHParams, device: str = "cuda:0"):
        super().__init__()

        self.event_dim = hparams.event_dim
        self.control_dim = hparams.control_dim
        self.init_dim = hparams.init_dim
        self.hidden_dim = hparams.hidden_dim
        self.gru_layers = hparams.gru_layers
        self.concat_dim = hparams.event_dim + 1 + hparams.control_dim
        self.input_dim = hparams.hidden_dim
        self.output_dim = hparams.event_dim

        self.primary_event = self.event_dim - 1

        self.device = device

        self.inithid_fc = nn.Linear(
            hparams.init_dim, hparams.gru_layers * hparams.hidden_dim
        )
        self.inithid_fc_activation = nn.Tanh()

        self.event_embedding = nn.Embedding(hparams.event_dim, hparams.event_dim)
        self.concat_input_fc = nn.Linear(self.concat_dim, self.input_dim)
        self.concat_input_fc_activation = nn.LeakyReLU(0.1, inplace=True)

        self.gru = nn.GRU(
            self.input_dim,
            self.hidden_dim,
            num_layers=hparams.gru_layers,
            dropout=hparams.gru_dropout,
        )
        self.output_fc = nn.Linear(
            hparams.hidden_dim * hparams.gru_layers, self.output_dim
        )
        self.output_fc_activation = nn.Softmax(dim=-1)

        self._initialize_weights()

    def _initialize_weights(self):
        nn.init.xavier_normal_(self.event_embedding.weight)
        nn.init.xavier_normal_(self.inithid_fc.weight)
        self.inithid_fc.bias.data.fill_(0.0)
        nn.init.xavier_normal_(self.concat_input_fc.weight)
        nn.init.xavier_normal_(self.output_fc.weight)
        self.output_fc.bias.data.fill_(0.0)

    def _sample_event(self, output, greedy=True, temperature=1.0):
        if greedy:
            return output.argmax(-1)
        output = output / temperature
        probs = self.output_fc_activation(output)
        return Categorical(probs).sample()

    def forward(self, event, control=None, hidden=None):
        # One step forward

        assert len(event.shape) == 2
        assert event.shape[0] == 1
        batch_size = event.shape[1]
        event = self.event_embedding(event)

        if control is None:
            default = torch.ones(1, batch_size, 1).to(self.device)
            control = torch.zeros(1, batch_size, self.control_dim).to(self.device)
        else:
            default = torch.zeros(1, batch_size, 1).to(self.device)
            assert control.shape == (1, batch_size, self.control_dim)

        concat = torch.cat([event, default, control], -1)
        inp = self.concat_input_fc(concat)
        inp = self.concat_input_fc_activation(inp)

        _, hidden = self.gru(inp, hidden)
        output = hidden.permute(1, 0, 2).contiguous()
        output = output.view(batch_size, -1).unsqueeze(0)
        output = self.output_fc(output)
        return output, hidden

    def get_primary_event(self, batch_size):
        return torch.LongTensor([[self.primary_event] * batch_size]).to(self.device)

    def init_to_hidden(self, init):
        # [batch_size, init_dim]
        batch_size = init.shape[0]
        out = self.inithid_fc(init)
        out = self.inithid_fc_activation(out)
        out = out.view(self.gru_layers, batch_size, self.hidden_dim)
        return out

    def expand_controls(self, controls, steps):
        # [1 or steps, batch_size, control_dim]
        assert len(controls.shape) == 3
        assert controls.shape[2] == self.control_dim
        if controls.shape[0] > 1:
            assert controls.shape[0] >= steps
            return controls[:steps]
        return controls.repeat(steps, 1, 1)

    def generate(
        self,
        init,
        steps,
        events=None,
        controls=None,
        greedy=1.0,
        temperature=1.0,
        teacher_forcing_ratio=1.0,
        output_type="index",
        verbose=False,
    ):
        # init [batch_size, init_dim]
        # events [steps, batch_size] indeces
        # controls [1 or steps, batch_size, control_dim]

        batch_size = init.shape[0]
        assert init.shape[1] == self.init_dim
        assert steps > 0

        use_teacher_forcing = events is not None
        if use_teacher_forcing:
            assert len(events.shape) == 2
            assert events.shape[0] >= steps - 1
            events = events[: steps - 1]

        event = self.get_primary_event(batch_size)
        use_control = controls is not None
        if use_control:
            controls = self.expand_controls(controls, steps)
        hidden = self.init_to_hidden(init)

        outputs = []
        step_iter = range(steps)
        if verbose:
            step_iter = Bar("Generating").iter(step_iter)

        for step in step_iter:
            control = controls[step].unsqueeze(0) if use_control else None
            output, hidden = self.forward(event, control, hidden)

            use_greedy = np.random.random() < greedy
            event = self._sample_event(
                output, greedy=use_greedy, temperature=temperature
            )

            if output_type == "index":
                outputs.append(event)
            elif output_type == "softmax":
                outputs.append(self.output_fc_activation(output))
            elif output_type == "logit":
                outputs.append(output)
            else:
                assert False

            if use_teacher_forcing and step < steps - 1:  # avoid last one
                if np.random.random() <= teacher_forcing_ratio:
                    event = events[step].unsqueeze(0)

        return torch.cat(outputs, 0)

    def beam_search(
        self,
        init,
        steps,
        beam_size,
        controls=None,
        temperature=1.0,
        stochastic=False,
        verbose=False,
    ):
        assert len(init.shape) == 2 and init.shape[1] == self.init_dim
        assert self.event_dim >= beam_size > 0 and steps > 0

        batch_size = init.shape[0]
        current_beam_size = 1

        if controls is not None:
            # [steps, batch_size, control_dim]
            controls = self.expand_controls(controls, steps)

        # Initial hidden weights
        # [gru_layers, batch_size, hidden_size]
        hidden = self.init_to_hidden(init)
        # [gru_layers, batch_size, 1, hidden_size]
        hidden = hidden[:, :, None, :]
        # [gru_layers, batch_size, beam_size, hidden_dim]
        hidden = hidden.repeat(1, 1, current_beam_size, 1)

        # Initial event
        event = self.get_primary_event(batch_size)  # [1, batch]
        event = event[:, :, None].repeat(1, 1, current_beam_size)  # [1, batch, 1]

        # [batch, beam, 1]   event sequences of beams
        beam_events = event[0, :, None, :].repeat(1, current_beam_size, 1)

        # [batch, beam] log probs sum of beams
        beam_log_prob = torch.zeros(batch_size, current_beam_size).to(self.device)

        if stochastic:
            # [batch, beam] Gumbel perturbed log probs of beams
            torch.zeros(batch_size, current_beam_size).to(self.device)
            torch.full((batch_size, beam_size), float("inf"))
            gumbel_dist = Gumbel(0, 1)

        step_iter = range(steps)
        if verbose:
            step_iter = Bar(["", "Stochastic "][stochastic] + "Beam Search").iter(
                step_iter
            )

        for step in step_iter:
            if controls is not None:
                # [1, batch, 1, control]
                control = controls[step, None, :, None, :]
                # [1, batch, beam, control]
                control = control.repeat(1, 1, current_beam_size, 1)
                # [1, batch*beam, control]
                control = control.view(
                    1, batch_size * current_beam_size, self.control_dim
                )
            else:
                control = None

            # [1, batch*beam0]
            event = event.view(1, batch_size * current_beam_size)
            # [grus, batch*beam, hid]
            hidden = hidden.view(
                self.gru_layers, batch_size * current_beam_size, self.hidden_dim
            )

            logits, hidden = self.forward(event, control, hidden)
            # [grus, batch, cbeam, hid]
            hidden = hidden.view(
                self.gru_layers, batch_size, current_beam_size, self.hidden_dim
            )
            logits = (logits / temperature).view(
                1, batch_size, current_beam_size, self.event_dim
            )

            beam_log_prob_expand = (
                logits + beam_log_prob[None, :, :, None]
            )  # [1, batch, cbeam, out]
            beam_log_prob_expand_batch = beam_log_prob_expand.view(
                1, batch_size, -1
            )  # [1, batch, cbeam*out]

            if stochastic:
                beam_log_prob_expand_perturbed = (
                    beam_log_prob_expand
                    + gumbel_dist.sample(beam_log_prob_expand.shape)
                )
                # [1, batch, cbeam]
                _, _ = beam_log_prob_expand_perturbed.max(-1)
                # print(beam_log_prob_Z)
                beam_log_prob_expand_perturbed_normalized = (
                    beam_log_prob_expand_perturbed
                )

                beam_log_prob_expand_perturbed_normalized_batch = (
                    beam_log_prob_expand_perturbed_normalized.view(1, batch_size, -1)
                )  # [1, batch, cbeam*out]
                _, top_indices = beam_log_prob_expand_perturbed_normalized_batch.topk(
                    beam_size, -1
                )  # [1, batch, cbeam]

                _ = torch.gather(
                    beam_log_prob_expand_perturbed_normalized_batch, -1, top_indices
                )[0]

            else:
                _, top_indices = beam_log_prob_expand_batch.topk(beam_size, -1)

            beam_log_prob = torch.gather(beam_log_prob_expand_batch, -1, top_indices)[
                0
            ]  # [batch, beam]

            beam_index_old = torch.arange(current_beam_size)[
                None, None, :, None
            ]  # [1, 1, cbeam, 1]
            beam_index_old = beam_index_old.repeat(
                1, batch_size, 1, self.output_dim
            )  # [1, batch, cbeam, out]
            beam_index_old = beam_index_old.view(
                1, batch_size, -1
            )  # [1, batch, cbeam*out]
            beam_index_new = torch.gather(beam_index_old, -1, top_indices)

            hidden = torch.gather(
                hidden, 2, beam_index_new[:, :, :, None].repeat(4, 1, 1, 1024)
            )

            event_index = torch.arange(self.output_dim)[
                None, None, None, :
            ]  # [1, 1, 1, out]
            event_index = event_index.repeat(
                1, batch_size, current_beam_size, 1
            )  # [1, batch, cbeam, out]
            event_index = event_index.view(1, batch_size, -1)  # [1, batch, cbeam*out]
            # [1, batch, cbeam*out]
            event = torch.gather(event_index, -1, top_indices)

            beam_events = torch.gather(
                beam_events[None],
                2,
                beam_index_new.unsqueeze(-1).repeat(1, 1, 1, beam_events.shape[-1]),
            )
            beam_events = torch.cat([beam_events, event.unsqueeze(-1)], -1)[0]

            current_beam_size = beam_size

        best = beam_events[torch.arange(batch_size).long(), beam_log_prob.argmax(-1)]
        best = best.contiguous().t()
        return best

    def inference(self, **kwargs):
        self.generate(**kwargs)
