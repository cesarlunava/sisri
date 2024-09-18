const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const axios = require('axios');

const app = express();

// Middleware para parsear datos del formulario
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json()); // Para trabajar con JSON

// Servir archivos estáticos como HTML, CSS, y fuentes
app.use(express.static(path.join(__dirname, 'public')));

// Ruta para mostrar el formulario de inicio de sesión
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

// Ruta para procesar los datos de inicio de sesión
app.post('/login', (req, res) => {
  const username = req.body.Nombre;
  const email = req.body.email;
  const password = req.body.password;

  // Aquí puedes validar los datos de inicio de sesión
  console.log('Nombre:', username);
  console.log('email:', email);
  console.log('contraseña:', password);

  // Redirigir al usuario a una página diferente después de iniciar sesión
  res.redirect('/dashboard.html');
});

// Ruta para mostrar el formulario de registro
app.get('/signup', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'signup.html'));
});

// Ruta para procesar los datos de registro
app.post('/signup', (req, res) => {
  const nombre = req.body.Nombre;
  const email = req.body.email;
  const password = req.body.password;

  // Aquí puedes procesar y almacenar los datos de registro
  console.log('Nombre:', nombre);
  console.log('Correo Electrónico:', email);
  console.log('Contraseña:', password);

  // Redirigir al usuario a una página diferente después del registro
  res.redirect('/login');
});

// Ruta del Dashboard (después de iniciar sesión)
app.get('/dashboard', (req, res) => {
  res.send('<h1>Bienvenido al Dashboard</h1>');
});

// Ruta para interactuar con Python
app.post('/procesar-con-python', (req, res) => {
  const data = req.body;

  // Hacer una solicitud POST a la API de Python
  axios.post('http://localhost:5000/procesar', data)
    .then(response => {
      console.log('Respuesta de Python:', response.data);
      res.send(response.data); // Devolver la respuesta al cliente
    })
    .catch(error => {
      console.error('Error al interactuar con Python:', error);
      res.status(500).send('Error al procesar los datos con Python');
    });
});

// Iniciar el servidor en el puerto 3000
app.listen(3000, () => {
  console.log('Servidor ejecutándose en http://localhost:3000');
});
