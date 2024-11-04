import React, { useState } from 'react';
import api from '../services/api';

const Register = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    access_level: 'common'
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/users/register', formData);
      alert(response.data.message);
      setFormData({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        access_level: 'common'
      });
    } catch (error) {
      if (error.response && error.response.data.message) {
        alert(error.response.data.message);
      } else {
        alert('Erro no registro');
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Registro</h2>
      <div>
        <label>Nome:</label>
        <input type="text" name="first_name" placeholder="Nome" value={formData.first_name}
          onChange={handleChange} required />
      </div>
      <div>
        <label>Sobrenome:</label>
        <input type="text" name="last_name" placeholder="Sobrenome" value={formData.last_name}
          onChange={handleChange} required />
      </div>
      <div>
        <label>Email:</label>
        <input type="email" name="email" placeholder="Email" value={formData.email}
          onChange={handleChange} required />
      </div>
      <div>
        <label>Senha:</label>
        <input type="password" name="password" placeholder="Senha" value={formData.password}
          onChange={handleChange} required />
      </div>
      <div>
        <label>Nível de Acesso:</label>
        <select name="access_level" value={formData.access_level} onChange={handleChange}>
          <option value="common">Comum</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <button type="submit">Registrar</button>
    </form>
  );
};

export default Register;
