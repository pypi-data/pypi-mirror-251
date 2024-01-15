import math
import nptyping
import numpy


class SparseSquareMatrix:
    """
    sparse square matrix class 
    """

    def __init__(self, row2idx, idx2col):
        ncols = row2idx.shape[0] - 1
        self.row2idx = row2idx
        self.idx2col = idx2col
        self.idx2val = numpy.zeros_like(idx2col, dtype=numpy.float64)
        self.row2val = numpy.zeros((ncols), dtype=numpy.float64)

    def set_zero(self):
        self.idx2val.fill(0.)
        self.row2val.fill(0.)

    # {y_vec} < - \alpha * [this_mat] * {x_vec} + \beta * {y_vec}
    def general_mult(
            self,
            alpha: float,
            x_vec: nptyping.NDArray[nptyping.Shape["*"], nptyping.Float],
            beta: float,
            y_vec: nptyping.NDArray[nptyping.Shape["*"], nptyping.Float]) -> None:
        assert x_vec.shape == y_vec.shape, "the shape of x_vector and y_vector should be the same"
        assert x_vec.shape[0] == self.row2idx.shape[0] - 1, "the size mismatch"
        if len(x_vec.shape) == 1 and len(y_vec.shape) == 1:
            from .del_ls import sparse_square_mult_vec
            sparse_square_mult_vec(
                self.row2idx, self.idx2col,
                self.row2val, self.idx2val,
                alpha, x_vec, beta, y_vec)
        elif len(x_vec.shape) == 2 and len(y_vec.shape) == 2:
            from .del_ls import sparse_square_mult_mat
            sparse_square_mult_mat(
                self.row2idx, self.idx2col,
                self.row2val, self.idx2val,
                alpha, x_vec, beta, y_vec)

    def solve_cg(
            self,
            r_vec: nptyping.NDArray[nptyping.Shape["*"], nptyping.Float],
            max_iteration=1000,
            conv_ratio_tol=1.0e-5):
        assert r_vec.shape[0] == self.row2idx.shape[0] - 1, "the size mismatch"
        u_vec = numpy.zeros_like(r_vec)
        p_vec = r_vec.copy()
        Ap_vec = numpy.zeros_like(r_vec)
        conv_hist = []
        sqnorm_res = numpy.sum(r_vec * r_vec)
        inv_sqnorm_res_ini = 1. / sqnorm_res
        for _iter in range(max_iteration):
            self.general_mult(1., p_vec, 0., Ap_vec)
            pap = numpy.sum(Ap_vec * p_vec)
            alpha = sqnorm_res / pap
            u_vec += alpha * p_vec
            r_vec -= alpha * Ap_vec
            sqnorm_res_new = numpy.sum(r_vec * r_vec)
            conv_ratio = math.sqrt(sqnorm_res_new * inv_sqnorm_res_ini)
            conv_hist.append(conv_ratio)
            if conv_ratio < conv_ratio_tol:
                return u_vec, conv_hist
            beta = sqnorm_res_new / sqnorm_res
            sqnorm_res = sqnorm_res_new
            p_vec = r_vec + beta * p_vec
        return u_vec, conv_hist
