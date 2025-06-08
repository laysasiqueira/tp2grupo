const express = require('express');
const axios = require('axios');
const router = express.Router();

// URL do servidor REST
const BASE_URL = 'http://192.168.246.62:5050';  // REST Flask

// Rota para obter contatos do servidor REST (GET)
router.get('/rest/contatos', async (req, res) => {
  try {
    const token = req.headers.authorization;
    console.log("🔐 Token recebido:", token);

    const resposta = await axios.get('http://192.168.246.62:5050/contatos', {
      headers: {
        Authorization: token
      }
    });

    res.json(resposta.data);
  } catch (error) {
    console.error("🔥 Erro ao obter contatos REST:");
    console.error("Mensagem:", error.message);
    if (error.response) {
      console.error("Status:", error.response.status);
      console.error("Data:", error.response.data);
    } else {
      console.error("Erro genérico:", error);
    }
    res.status(500).json({ erro: "Erro ao obter contatos REST" });
  }
});

// Rota para adicionar um novo contato no servidor REST (POST)
router.post('/rest/contatos', async (req, res) => {
  try {
    const novoContato = req.body;
    const resposta = await axios.post(`${BASE_URL}/contatos`, novoContato, {
      headers: {
        Authorization: req.headers.authorization
      }
    });
    res.status(201).json(resposta.data);
  } catch (error) {
    console.error('Erro ao adicionar contato REST:', error.message);
    res.status(500).json({ erro: 'Erro ao adicionar contato REST' });
  }
});

// Rota para apagar um contato do servidor REST (DELETE)
router.delete('/rest/contatos/:id', async (req, res) => {
  try {
    const { id } = req.params;
    await axios.delete(`${BASE_URL}/contatos/${id}`, {
      headers: {
        Authorization: req.headers.authorization
      }
    });
    res.status(204).send();  // sucesso sem conteúdo
  } catch (error) {
    console.error('Erro ao apagar contato REST:', error.message);
    res.status(500).json({ erro: 'Erro ao apagar contato REST' });
  }
});

module.exports = router;
