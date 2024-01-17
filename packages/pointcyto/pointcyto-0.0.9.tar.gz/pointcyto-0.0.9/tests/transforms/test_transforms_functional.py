from unittest import TestCase

import torch

import pointcyto.transforms.transforms_functional as t_func


class TestTransformsFunctional(TestCase):
    def test_asinh(self):
        torch.manual_seed(23178)
        x = torch.randn((3, 2))
        target = torch.tensor(
            [
                [-1.02025531310114, 0.650699301054285],
                [0.156954780747593, 0.646511502753712],
                [0.896005194544506, -0.591923641697527],
            ]
        )
        # target via R:
        # x = matrix(c(-1.2067, 0.6976,
        #              0.1576, 0.6925,
        #              1.0208, -0.6271), ncol=2, byrow=TRUE)
        # calced = asinh(x)
        # Rvarious::print_as_python(calced)
        assert torch.allclose(t_func.arcsinh(x), target, atol=1e-4)

    def test_asinh_param(self):
        torch.manual_seed(23178)
        x = torch.randn((3, 2))

        # target via R:
        # x = matrix(c(-1.2067, 0.6976,
        #              0.1576, 0.6925,
        #              1.0208, -0.6271), ncol=2, byrow=TRUE)
        # a = 1
        # b = 1
        # c = 2
        # calced = asinh(a + b * x) + c
        # Rvarious::print_as_python(calced)
        target = torch.tensor(
            [
                [1.7947442733302, 3.29960294002619],
                [2.98854374326608, 3.29701153276323],
                [3.45289900843958, 2.3647576349827],
            ]
        )
        assert torch.allclose(t_func.arcsinh_param(x, 1, 1, 2), target, atol=1e-4)
