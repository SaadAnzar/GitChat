import React from 'react'
import { BsArrowReturnRight } from 'react-icons/bs'
import Chatgpt from '../components/Chatgpt'

const AskGitHub = () => {
  const [input, setInput] = React.useState('')

  return (
    <div className="max-h-screen flex flex-col w-full sm:p-8 p-2">
      <div className="sm:flex justify-between">
        <div className="sm:w-[45%] p-2">
          <div className="bg-gray-gradient m-2 rounded-lg z-1 py-2 drop-shadow-md">
            <form>
              <div className="px-4 py-2 flex items-center">
                <input
                  type="text"
                  value={input}
                  placeholder="Enter or Paste the GitHub URL here..."
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
          <div className="bg-gray-gradient rounded-lg z-1 py-2 mx-2 my-0.5 drop-shadow-md">
            <div className="px-4 py-2">
              <div className="bg-inherit border-none outline-none text-gray-400 w-full placeholder:text-[#707070]">
                <p>
                  <span className="text-gray-700 font-semibold">Title:</span>{' '}
                  <span className="text-gray-400">
                    Title of the GitHub Repo
                  </span>
                </p>
                <p>
                  <span className="text-gray-700 font-semibold">
                    Description:
                  </span>{' '}
                  <span className="text-gray-400">
                    Description of the GitHub Repo
                  </span>
                </p>
                <p>
                  <span className="text-gray-700 font-semibold">Language:</span>{' '}
                  <span className="text-gray-400">
                    Language of the GitHub Repo
                  </span>
                </p>
                <p>
                  <span className="text-gray-700 font-semibold">Stars:</span>{' '}
                  <span className="text-gray-400">
                    Stars of the GitHub Repo
                  </span>
                </p>
                <p>
                  <span className="text-gray-700 font-semibold">Forks:</span>{' '}
                  <span className="text-gray-400">
                    Forks of the GitHub Repo
                  </span>
                </p>
                <p>
                  <span className="text-gray-700 font-semibold">License:</span>{' '}
                  <span className="text-gray-400">
                    License of the GitHub Repo
                  </span>
                </p>
                <p>
                  <span className="text-gray-700 font-semibold">URL:</span>{' '}
                  <span className="text-gray-400">URL of the GitHub Repo</span>
                </p>
              </div>
            </div>
          </div>
        </div>
        <div className="sm:w-[45%] p-2">
          <Chatgpt />
        </div>
      </div>
    </div>
  )
}

export default AskGitHub
