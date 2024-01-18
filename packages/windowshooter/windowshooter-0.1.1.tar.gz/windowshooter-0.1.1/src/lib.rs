use pyo3::prelude::*;

use numpy::pyo3::Python;
use numpy::PyArray3;

use mimalloc::MiMalloc;

#[global_allocator]
static GLOBAL: MiMalloc = MiMalloc;

#[pyclass]
struct Window(screenshot::Window);

#[pyclass]
struct Shooter(screenshot::Recorder);

#[pymethods]
impl Window {
    #[new]
    fn new(window_name: String) -> Self {
        Window(screenshot::Window::new_from_name(window_name).unwrap())
    }
}
#[pymethods]
impl Shooter {
    #[new]
    fn new(window: &Window) -> Self {
        Shooter(window.0.create_record().unwrap())
    }
    fn numpy_screenshot<'py>(&self, py: Python<'py>) -> PyResult<&'py PyArray3<u8>> {
        let data = self.0.get_image().unwrap();

        Ok(numpy::PyArray3::from_owned_array(py, data))
    }
}

#[pymodule]
fn windowshooter(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Shooter>()?;
    m.add_class::<Window>()?;
    Ok(())
}

/*#[pyfunction]
fn take_screenshot() -> PyResult<Vec<Vec<(u8, u8, u8, u8)>>> {
    Ok(screenshot::take_screenshot().unwrap())
}*/
