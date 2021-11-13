import { Component } from 'react';
import '../css/mirillaPage.css';
import Navigation from './navbar';
import CodeMirror from '@uiw/react-codemirror';
import 'codemirror/theme/dracula.css';
import 'codemirror/theme/base16-light.css';
import 'codemirror/addon/hint/show-hint';
import 'codemirror/addon/hint/javascript-hint';
import 'codemirror/addon/hint/show-hint.css';
import 'codemirror/addon/hint/anyword-hint';
import 'codemirror/keymap/sublime';
import 'codemirror/addon/edit/closebrackets';
import 'codemirror/addon/edit/closetag';
import 'codemirror/addon/fold/foldcode';
import 'codemirror/addon/fold/foldgutter';
import 'codemirror/addon/fold/brace-fold';
import 'codemirror/addon/fold/comment-fold';
import 'codemirror/addon/fold/foldgutter.css';

export default class Compiler extends Component {

    constructor() {
        super();

        this.state = {
            entrada: '',
            salida: ''
        };

        this.compiler = this.compiler.bind(this)
    }

    compiler(){
        fetch('https://jolc2-back-201900874.herokuapp.com/Mirilla', {
            method: 'POST',
            body: JSON.stringify(this.state),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            this.setState({
                salida: data.salida
            })
        });
    }
    
    render() {
        return(
            <div>
                <div>
                    <Navigation/>
                </div>

                <h3 id = "entrada">Entrada</h3>
                <div id = "compiler">
                    <CodeMirror
                        value={ this.state.entrada }
                        options={{
                            mode: 'go',
                            theme: 'dracula',
                            smartIndent: true,
                            lineNumbers: true,
                            foldGutter: true,
                            gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
                            autoCloseTags: true,
                            matchBrackets: true,
                            autoCloseBrackets: true
                        }}
                        onChange = {(editor, data, value) => {
                            this.setState({
                                entrada: editor.getValue()
                            });
                        }}
                    />
                </div>

                <h3 id = "salida">Salida</h3>
                <div id = "console">
                <CodeMirror
                        value={ this.state.salida }
                        options={{
                            mode: 'x-rst',
                            theme: 'base16-light',
                            lineNumbers: false,
                            readOnly: true
                        }}
                    />
                </div>

                <button onClick={this.compiler} id = "buttonCompiler">Optimizar</button>

                
            </div>
        );
    }
}