import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import Chatgpt from '../components/Chatgpt'

const AskGitHub = () => {
  const [url, setUrl] = useState('')

  return (
    <div className="max-h-screen flex flex-col w-full sm:px-8 sm:py-4 p-2">
      <div className="flex flex-row gap-x-20 items-center">
        <h1 className="sm:mx-20 text-xl font-bold text-gray-500 text-center">
          Enter or Paste the GitHub URL and ask questions regarding it
        </h1>
        <Link
          to="/chatcode"
          className="px-4 py-2 bg-[#FF9500] text-white rounded-lg"
        >
          Chat with Code
        </Link>
      </div>
      <div className="bg-gray-gradient mx-4 mt-2 rounded-lg z-1 py-2 drop-shadow-md">
        <div className="px-4 py-1 flex items-center">
          <input
            type="text"
            value={url}
            placeholder="Enter or Paste the GitHub URL here..."
            onChange={(event) => setUrl(event.target.value)}
            className="bg-inherit border-none outline-none text-gray-400 w-full placeholder:text-[#707070]"
          />
        </div>
      </div>
      <Chatgpt url={url} />
    </div>
  )
}

export default AskGitHub
