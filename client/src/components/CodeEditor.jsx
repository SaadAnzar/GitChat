import React, { useState } from 'react'
import Editor from 'react-simple-code-editor'
import { highlight, languages } from 'prismjs/components/prism-core'
import 'prismjs/components/prism-clike'
import 'prismjs/components/prism-javascript'

// const codeSnippet = `function add(a, b) {
//   return a + b;
// }

// add(5, 10);
// // Output: 15
// `

function CodeEditor({ code, setCode }) {
  // const [code, setCode] = useState(codeSnippet)

  return (
    <div className="App">
      <div className="window">
        <div className="title-bar">
          <div className="title-buttons">
            <div className="title-button"></div>
            <div className="title-button"></div>
            <div className="title-button"></div>
          </div>
        </div>
        <div className="editor_wrap">
          <Editor
            value={code}
            onValueChange={(code) => setCode(code)}
            highlight={(code) => highlight(code, languages.js)}
            padding={10}
            style={{
              fontFamily: '"Fira code", "Fira Mono", monospace',
              fontSize: 12,
            }}
          />
        </div>
      </div>
    </div>
  )
}

export default CodeEditor
