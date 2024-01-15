/// A Python module implemented in Rust.
#[pyo3::pymodule]
#[pyo3(name = "del_ls")]
fn del_ls_(
    _py: pyo3::Python,
    m: &pyo3::types::PyModule)
    -> pyo3::PyResult<()>
{
    /// compute the matrix-vector multiplication \alpha * [A] * {x} + \beta * {y}
    #[pyfn(m)]
    fn sparse_square_mult_vec(
        row2idx: numpy::PyReadonlyArray1<usize>,
        idx2col: numpy::PyReadonlyArray1<usize>,
        row2val: numpy::PyReadonlyArray1<f64>,
        idx2val: numpy::PyReadonlyArray1<f64>,
        alpha: f64,
        x_vec: numpy::PyReadonlyArray1<f64>,
        beta: f64,
        mut y_vec: numpy::PyReadwriteArray1<f64>)
    {
        let num_row = row2idx.len() - 1;
        assert_eq!(y_vec.len(), num_row);
        assert_eq!(x_vec.len(), num_row);
        assert_eq!(row2val.len(), num_row);
        let y_vec = y_vec.as_slice_mut().unwrap();
        let row2idx = row2idx.as_slice().unwrap();
        let idx2col = idx2col.as_slice().unwrap();
        let idx2val = idx2val.as_slice().unwrap();
        let row2val = row2val.as_slice().unwrap();
        let x_vec = x_vec.as_slice().unwrap();
        for val_y in y_vec.iter_mut() { *val_y *= beta; };
        for i_row in 0..num_row {
            for idx in row2idx[i_row]..row2idx[i_row + 1] {
                let j_col = idx2col[idx];
                y_vec[i_row] += alpha * idx2val[idx] * x_vec[j_col];
            }
            y_vec[i_row] += alpha * row2val[i_row] * x_vec[i_row];
        }
    }

    /// compute the matrix-vector multiplication \alpha * [A] * [x] + \beta * [y]
    #[pyfn(m)]
    fn sparse_square_mult_mat(
        row2idx: numpy::PyReadonlyArray1<usize>,
        idx2col: numpy::PyReadonlyArray1<usize>,
        row2val: numpy::PyReadonlyArray1<f64>,
        idx2val: numpy::PyReadonlyArray1<f64>,
        alpha: f64,
        x_mat: numpy::PyReadonlyArray2<f64>,
        beta: f64,
        mut y_mat: numpy::PyReadwriteArray2<f64>)
    {
        let num_row = row2idx.len() - 1;
        assert_eq!(y_mat.shape()[0], num_row);
        assert_eq!(x_mat.shape()[0], num_row);
        assert_eq!(x_mat.shape()[1], y_mat.shape()[1]);
        assert_eq!(row2val.len(), row2idx.len()-1);
        let ydim = y_mat.shape()[1];
        let y_mat = y_mat.as_slice_mut().unwrap();
        let row2idx = row2idx.as_slice().unwrap();
        let idx2col = idx2col.as_slice().unwrap();
        let idx2val = idx2val.as_slice().unwrap();
        let row2val = row2val.as_slice().unwrap();
        let x_mat = x_mat.as_slice().unwrap();
        for val_y in y_mat.iter_mut() { *val_y *= beta; };
        for i_row in 0..num_row {
            for idx in row2idx[i_row]..row2idx[i_row + 1] {
                let j_col = idx2col[idx];
                for y in 0..ydim {
                    y_mat[i_row * ydim + y] += alpha * idx2val[idx] * x_mat[j_col * ydim + y];
                }
            }
            for y in 0..ydim {
                y_mat[i_row * ydim + y] += alpha * row2val[i_row] * x_mat[i_row * ydim + y];
            }
        }
    }

    Ok(())
}