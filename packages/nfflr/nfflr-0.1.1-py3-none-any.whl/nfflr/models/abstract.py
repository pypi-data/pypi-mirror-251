from plum import dispatch
from torch import nn

from nfflr.data.atoms import Atoms


class AbstractModel(nn.Module):
    @dispatch
    def forward(self, x):
        """Fallback method"""
        print("fallback")
        self.forward(Atoms(x))
