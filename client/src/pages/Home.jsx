import React from 'react'
import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <div className="h-screen">
      <div className="flex flex-col justify-center items-center h-full">
        <div className="text-4xl font-bold">Welcome to CodeBot</div>
        <div className="text-2xl font-medium mt-4">
          A chatbot that helps you with your code
        </div>
        <div className="mt-8">
          <Link
            to="/chatcode"
            className="px-4 py-2 bg-[#FF9500] text-white rounded-lg"
          >
            Get Started
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Home
