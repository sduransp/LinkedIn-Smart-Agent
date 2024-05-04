import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        // Aquí se haría la llamada al backend para verificar los datos
        // Ejemplo: axios.post('/api/login', { username, password })
        // .then(response => {
        //   // Guardar el token en localStorage o manejar la sesión
        //   navigate('/home');
        // })
        // .catch(error => {
        //   console.error('Error de autenticación', error);
        // });
        console.log('Logging in:', username, password);
        // Navegar a la página principal
        navigate(process.env.PUBLIC_URL + '/');
    };

    return (
        <div className='background' style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
                <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default LoginPage;
