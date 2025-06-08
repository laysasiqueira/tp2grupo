const express = require('express');
const axios = require('axios');
const router = express.Router();

const AUTH_URL = 'http://192.168.246.62:6000';

router.post('/auth/login', async (req, res) => {
  try {
    const resposta = await axios.post(`${AUTH_URL}/login`, req.body);
    res.json(resposta.data);
  } catch (error) {
    console.error('Erro no login:', error.message);
    res.status(401).json({ erro: 'Credenciais inválidas' });
  }
});

module.exports = router;
