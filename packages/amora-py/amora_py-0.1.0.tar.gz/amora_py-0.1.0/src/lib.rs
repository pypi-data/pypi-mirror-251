//  This Source Code Form is subject to the terms of the Mozilla Public
//  License, v. 2.0. If a copy of the MPL was not distributed with this
//  file, You can obtain one at http://mozilla.org/MPL/2.0/.

use amora_rs;
use x25519_dalek::{PublicKey, StaticSecret};
use pyo3::prelude::*;
use pyo3::PyResult;
use pyo3::exceptions::PyValueError;

#[pymodule]
fn amora_py(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
	m.add_class::<Amora>()?;
	Ok(())
}

#[pyclass]
struct Amora {
	amora: amora_rs::Amora,
}

#[pymethods]
impl Amora {
	#[staticmethod]
	fn amora_zero(key: [u8; 32]) -> Amora {
		let amora = amora_rs::Amora::amora_zero(&key);
		Amora { amora: amora }
	}

	#[staticmethod]
	fn amora_one(secret_key: Option<[u8; 32]>, public_key: Option<[u8; 32]>) -> Amora {
		let secret_key: Option<StaticSecret> = match secret_key {
			Some(key) => Some(StaticSecret::from(key)),
			None => None,
		};

		let public_key: Option<PublicKey> = match public_key {
			Some(key) => Some(PublicKey::from(key)),
			None => None,
		};

		let amora = amora_rs::Amora::amora_one(secret_key, public_key);
		Amora { amora: amora }
	}

	#[staticmethod]
	fn amora_zero_from_str(key: &str) -> PyResult<Amora> {
		match amora_rs::Amora::amora_zero_from_str(key) {
			Ok(amora) => Ok(Amora { amora: amora }),
			Err(error) => Err(PyValueError::new_err(format!("{:?}", error))),
		}
	}

	#[staticmethod]
	fn amora_one_from_str(secret_key: Option<&str>, public_key: Option<&str>)
		-> PyResult<Amora> {

		match amora_rs::Amora::amora_one_from_str(secret_key, public_key) {
			Ok(amora) => Ok(Amora { amora: amora }),
			Err(error) => Err(PyValueError::new_err(format!("{:?}", error))),
		}
	}

	fn encode(&self, payload: &[u8], ttl: u32) -> String {
		self.amora.encode(payload, ttl)
	}

	fn decode(&self, token: &str, validate: bool) -> PyResult<Vec<u8>> {
		match self.amora.decode(token, validate) {
			Ok(decoded) => Ok(decoded),
			Err(error) => Err(PyValueError::new_err(format!("{:?}", error))),
		}
	}
}
