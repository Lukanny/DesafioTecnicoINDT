import React, { useState } from 'react';
import api from '../services/api';

const Login = ({ setAuth }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/users/login', { email, password });
      localStorage.setItem('token', response.data.access_token);
      setAuth(true);
    } catch (error) {
      alert('Credenciais inválidas');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      <div>
        <label>Email:</label>
        <input type="email" placeholder="Email" value={email}
          onChange={(e) => setEmail(e.target.value)} required />
      </div>
      <div>
        <label>Senha:</label>
        <input type="password" placeholder="Senha" value={password}
          onChange={(e) => setPassword(e.target.value)} required />
      </div>
      <button type="submit">Entrar</button>
    </form>
  );
};

export default Login;
