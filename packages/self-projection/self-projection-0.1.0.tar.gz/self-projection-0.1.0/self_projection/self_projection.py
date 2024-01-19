import torch
import torch.nn as nn


from typing import Union


class SelfProjection(nn.Module):
    size_input: Union[torch.Size, list[int]]
    size_projection: int
    eps: float

    # Normalizations params.
    gamma_o_sum: nn.Parameter
    gamma_o: nn.Parameter
    gamma_p_sum: nn.Parameter
    gamma_p: nn.Parameter
    gamma: nn.Parameter
    beta_o_sum: nn.Parameter
    beta_o: nn.Parameter
    beta_p_sum: nn.Parameter
    beta_p: nn.Parameter
    beta: nn.Parameter

    # Permutations params.
    original_xj_y: nn.Parameter
    original_xi_y: nn.Parameter
    permuted_xj_y: nn.Parameter
    permuted_xi_y: nn.Parameter

    def __init__(
        self,
        size_input: Union[torch.Size, list[int]],
        size_projection: int,
        eps: float = 1e-5,
        **kwargs,
    ) -> None:
        super(SelfProjection, self).__init__(**kwargs)

        # Define internal variables.
        self.size_input = (
            size_input if isinstance(size_input, torch.Size) else torch.Size(size_input)
        )
        self.size_projection = size_projection
        self.eps = eps

        # Define trainable parameters: normalizations.
        self.gamma_o_sum = nn.Parameter(torch.ones([size_projection]))
        self.gamma_o = nn.Parameter(torch.ones([size_projection, size_projection]))
        self.gamma_p_sum = nn.Parameter(torch.ones([size_projection]))
        self.gamma_p = nn.Parameter(torch.ones([size_projection, size_projection]))
        self.gamma = nn.Parameter(torch.ones([size_projection, size_projection]))

        self.beta_o_sum = nn.Parameter(torch.zeros([size_projection]))
        self.beta_o = nn.Parameter(torch.zeros([size_projection, size_projection]))
        self.beta_p_sum = nn.Parameter(torch.zeros([size_projection]))
        self.beta_p = nn.Parameter(torch.zeros([size_projection, size_projection]))
        self.beta = nn.Parameter(torch.zeros([size_projection, size_projection]))

        # Define trainable parameters: permutations.
        original_xj_y = torch.empty([self.size_input[1], self.size_projection])
        original_xj_y = nn.init.xavier_uniform_(original_xj_y)
        self.original_xj_y = nn.Parameter(original_xj_y)

        original_xi_y = torch.empty([self.size_input[0], self.size_projection])
        original_xi_y = nn.init.xavier_uniform_(original_xi_y)
        self.original_xi_y = nn.Parameter(original_xi_y)

        permuted_xj_y = torch.empty([self.size_input[0], self.size_projection])
        permuted_xj_y = nn.init.xavier_uniform_(permuted_xj_y)
        self.permuted_xj_y = nn.Parameter(permuted_xj_y)

        permuted_xi_y = torch.empty([self.size_input[1], self.size_projection])
        permuted_xi_y = nn.init.xavier_uniform_(permuted_xi_y)
        self.permuted_xi_y = nn.Parameter(permuted_xi_y)

        pass

    def _normalize(
        self,
        x: torch.FloatTensor,
        dims: list[int],
        gamma: nn.Parameter,
        beta: nn.Parameter,
    ) -> torch.FloatTensor:
        mean = x.mean(dim=dims, keepdim=True)
        std = x.std(dim=dims, keepdim=True)
        y = (x - mean) / (std + self.eps)
        norm = gamma * y + beta
        return norm

    def forward(
        self,
        x: torch.FloatTensor,
    ) -> torch.FloatTensor:
        # Define initial projections.
        original = x
        permuted = x.permute([0, -1, -2])

        # Original projection.
        original_yy = original @ self.original_xj_y
        original_sum = original_yy.sum(dim=-2)
        original_sum = self._normalize(
            x=original_sum,
            dims=[-1],
            gamma=self.gamma_o_sum,
            beta=self.beta_o_sum,
        )
        original_sum = original_sum.add(1.0)
        original_yy = original_yy.permute([0, -1, -2]) @ self.original_xi_y
        original_yy = original_yy.permute([0, -1, -2])
        original_yy = self._normalize(
            x=original_yy,
            dims=[-1, -2],
            gamma=self.gamma_o,
            beta=self.beta_o,
        )

        # Permuted projection.
        permuted_yy = permuted @ self.permuted_xj_y
        permuted_sum = permuted_yy.sum(dim=-2)
        permuted_sum = self._normalize(
            x=permuted_sum,
            dims=[-1],
            gamma=self.gamma_p_sum,
            beta=self.beta_p_sum,
        )
        permuted_sum = permuted_sum.add(1.0)
        permuted_yy = permuted_yy.permute([0, -1, -2]) @ self.permuted_xi_y
        permuted_yy = permuted_yy.permute([0, -1, -2])
        permuted_yy = self._normalize(
            x=permuted_yy,
            dims=[-1, -2],
            gamma=self.gamma_p,
            beta=self.beta_p,
        )

        # Self-project.
        relations = torch.einsum("ij,ik->ijk", original_sum, permuted_sum)
        projected = original_yy.mul(relations) @ permuted_yy.mul(relations)
        projected = self._normalize(
            x=projected,
            dims=[-1, -2],
            gamma=self.gamma,
            beta=self.beta,
        )

        return projected, relations
