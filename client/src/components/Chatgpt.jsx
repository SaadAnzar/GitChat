import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { questions } from '../data'
import { BsArrowReturnRight } from 'react-icons/bs'
import { AiFillDelete } from 'react-icons/ai'

const Chatgpt = ({ code }) => {
  const [input, setInput] = useState('')
  const [chats, setChats] = useState(
    JSON.parse(localStorage.getItem('chats')) || [
      { message: 'Hello, I am a chatbot. How can I help you?', author: 'bot' },
    ]
  )

  // Make a button to clear the chats
  const handleClearChats = () => {
    localStorage.removeItem('chats')
    setChats([
      { message: 'Hello, I am a chatbot. How can I help you?', author: 'bot' },
    ])
  }

  const chatContainerRef = useRef(null)

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
    }
    // Store the chats data in local storage
    localStorage.setItem('chats', JSON.stringify(chats))
  }, [chats])

  const handleSubmit = (event) => {
    event.preventDefault()

    setChats([...chats, { message: input, author: 'user' }])
  }

  const handleQuestionClick = (question) => {
    setChats([...chats, { message: question, author: 'user' }])
  }

  return (
    <div className="mx-2">
      <div
        ref={chatContainerRef}
        className="bg-gray-gradient mx-2 mt-2 sm:h-[59vh] h-auto overflow-y-auto shadow rounded-lg"
      >
        {chats.map((chat, index) => (
          <div
            key={index}
            className={`py-0.5 rounded-lg mx-2.5 my-2 ${
              chat.author === 'user' ? 'text-right' : 'text-left w-[90%]'
            }`}
          >
            <span
              className={`inline-block px-2 py-0.5 text-base font-medium rounded-lg ${
                chat.author === 'user'
                  ? 'bg-[#FFEFD9] text-[#FF9500] rounded-br-none'
                  : 'bg-gray-200 text-gray-700 rounded-bl-none'
              }`}
            >
              {chat.message}
            </span>
          </div>
        ))}
      </div>

      <div className="flex flex-col">
        {questions.map((question, index) => (
          <button
            key={index}
            onClick={() => handleQuestionClick(question.question)}
            className="bg-gray-gradient rounded-lg z-1 py-2 mx-2 my-0.5 drop-shadow-md"
          >
            {question.question}
          </button>
        ))}
        <div className="flex justify-between">
          <div className=" bg-gray-gradient m-2 rounded-lg z-1 py-2 drop-shadow-md w-[90%]">
            <form onSubmit={handleSubmit}>
              <div className="px-4 py-2 flex items-center">
                <input
                  type="text"
                  value={input}
                  placeholder="Ask about the code here..."
                  onChange={(event) =>
                    setInput(
                      event.target.value.charAt(0).toUpperCase() +
                        event.target.value.slice(1)
                    )
                  }
                  className="bg-inherit border-none outline-none text-gray-400 w-full placeholder:text-[#707070]"
                />
                <button type="submit" className="ml-2 text-gray-300">
                  <BsArrowReturnRight />
                </button>
              </div>
            </form>
          </div>
          <div className="flex bg-gray-gradient text-red-500 p-4 m-2 rounded-lg z-1 py-2 drop-shadow-md w-auto items-center">
            <button
              onClick={handleClearChats}
              className="hover:scale-150 transition-all"
            >
              <AiFillDelete />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Chatgpt
