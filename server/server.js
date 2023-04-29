import express from 'express'
import * as dotenv from 'dotenv'
import cors from 'cors'
import { Configuration, OpenAIApi } from 'openai'

dotenv.config()

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
})

const openai = new OpenAIApi(configuration)

const app = express()
app.use(cors())
app.use(express.json())

app.get('/', async (req, res) => {
  res.status(200).send({
    message: 'Hello from CodeHub! The server is working fine.',
  })
})

// Chatbot API
app.post('/chat', async (req, res) => {
  try {
    const chat = req.body.prompt
    const code = req.body.code
    // console.log(chat);

    const response = await openai.createCompletion({
      model: 'text-davinci-003',
      prompt: `Take the following code as input:\n${code}\n and then answer the following question in reference to the code given above:\n${chat}\n`,
      temperature: 0.9,
      max_tokens: 150,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0.6,
      stop: ['You:'],
    })

    res.status(200).send({
      answer: response.data.choices[0].text,
    })
  } catch (error) {
    console.error(error)
    res.status(500).send(error)
  }
})

app.listen(5000, () =>
  console.log('Server started at http://localhost:5000. Enjoy!')
)
