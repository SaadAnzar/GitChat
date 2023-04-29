import React, { useState } from 'react'
import Chatbot from '../components/Chatbot'
import CodeEditor from '../components/CodeEditor'

const CodeSnippet = `function add(a, b) {
  return a + b;
}

add(5, 10);
// Output: 15
`

const ChatCode = () => {
  const [code, setCode] = useState(CodeSnippet)

  return (
    <div className="max-h-screen flex flex-col w-full sm:p-8 p-2">
      <div className="sm:flex justify-between">
        <div className="sm:w-[45%] p-2">
          <CodeEditor code={code} setCode={setCode} />
        </div>
        <div className="sm:w-[45%] p-2">
          <Chatbot code={code} />
        </div>
      </div>
    </div>
  )
}

export default ChatCode
