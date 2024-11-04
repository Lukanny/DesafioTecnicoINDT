import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import UserList from './components/UserList';
import UserStats from './components/UserStats';
import api from './services/api';

function App() {
    const [auth, setAuth] = useState(false);
    const [user, setUser] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            setAuth(true);
            const payload = JSON.parse(atob(token.split('.')[1]));
            setUser(payload.identity);
        }
    }, []);

    const PrivateRoute = ({ children }) => {
        return auth ? children : <Navigate to="/login" />;
    };

    const AdminRoute = ({ children }) => {
        return auth && user && user.access_level === 'admin' ? children : <Navigate to="/" />;
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setAuth(false);
        setUser(null);
    };

    return (
        <Router>
            <div className="container">
                <Routes>
                    <Route path="/login" element={<Login setAuth={setAuth} />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/" element={
                        <PrivateRoute>
                            <div>
                                <h1>Bem-vindo ao Sistema de Gerenciamento de Usuários</h1>
                                <button onClick={handleLogout}>Logout</button>
                                {user && user.access_level === 'admin' && (
                                    <div>
                                        <h2>Painel Administrativo</h2>
                                        <UserStats />
                                        <UserList />
                                    </div>
                                )}
                            </div>
                        </PrivateRoute>
                    } />
                    <Route path="*" element={<Navigate to="/" />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
