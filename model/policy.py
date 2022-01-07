import torch
import torch.nn as nn


class DefaultPolicy(nn.Module):
    def __init__(self, hidden_size_pol, hidden_size):
        super(DefaultPolicy, self).__init__()
        self.hidden_size = hidden_size


        self.W_u = nn.Linear(hidden_size, hidden_size_pol, bias=False)
        # self.W_bs = nn.Linear(bs_size, hidden_size_pol, bias=False)
        # self.W_db = nn.Linear(db_size, hidden_size_pol, bias=False)

    def forward(self, encodings, act_tensor=None):
        if isinstance(encodings, tuple):
            hidden = encodings[0]
        else:
            hidden = encodings

        # Network based
        output = self.W_u(hidden[0])
        output = torch.tanh(output)

        if isinstance(encodings, tuple):  # return LSTM tuple
            return (output.unsqueeze(0), encodings[1])
        else:
            return output.unsqueeze(0)

