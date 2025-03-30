const vscode = require('vscode');
// const path = require('path');
// const fs = require('fs');

function getSceneName(document, lineNumber) {
    // Find the class definition before the current line
    let text = document.getText();
    let lines = text.split('\n');
    
    for (let i = lineNumber; i >= 0; i--) {
        let match = lines[i].match(/class\s+(\w+)\s*\(\s*\w+\s*\)/);
        if (match) {
            return match[1];
        }
    }
    return null;
}

function activate(context) {
    // Run Scene command
    let runScene = vscode.commands.registerCommand('manimCursor.runScene', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;

        const document = editor.document;
        const filePath = document.fileName;
        const position = editor.selection.active;
        const lineNumber = position.line + 1;
        const sceneName = getSceneName(document, position.line);
        
        if (!sceneName) {
            vscode.window.showErrorMessage('No scene class found');
            return;
        }
        
        // Save the file
        document.save();
        
        // Create terminal if it doesn't exist
        let terminal = vscode.window.terminals.find(t => t.name === 'Manim');
        if (!terminal) {
            terminal = vscode.window.createTerminal('Manim');
        }
        
        terminal.show();
        
        // Run the command
        const command = `manimgl "${filePath}" ${sceneName} -se ${lineNumber}`;
        terminal.sendText(command);
    });

    // Checkpoint Paste command
    let checkpointPaste = vscode.commands.registerCommand('manimCursor.checkpointPaste', function () {
        sendCheckpointPaste();
    });

    // Recorded Checkpoint Paste command
    let recordedCheckpointPaste = vscode.commands.registerCommand('manimCursor.recordedCheckpointPaste', function () {
        sendCheckpointPaste('record=True');
    });

    // Skipped Checkpoint Paste command
    let skippedCheckpointPaste = vscode.commands.registerCommand('manimCursor.skippedCheckpointPaste', function () {
        sendCheckpointPaste('skip=True');
    });

    // Exit command
    let exit = vscode.commands.registerCommand('manimCursor.exit', function () {
        let terminal = vscode.window.terminals.find(t => t.name === 'Manim');
        if (terminal) {
            terminal.sendText('\x03quit');
        }
    });

    // New command to run the current line
    let runCurrentLine = vscode.commands.registerCommand('manimCursor.runCurrentLine', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;

        // Get the current line
        const document = editor.document;
        const position = editor.selection.active;
        const line = document.lineAt(position.line);
        const lineText = line.text.trim();

        if (!lineText) {
            vscode.window.showErrorMessage('Current line is empty');
            return;
        }

        // Select the current line
        const selection = new vscode.Selection(
            position.line, 0,
            position.line, line.text.length
        );
        editor.selection = selection;

        // Find the terminal or create it
        let terminal = vscode.window.terminals.find(t => t.name === 'Manim');
        if (!terminal) {
            terminal = vscode.window.createTerminal('Manim');
        }
        
        terminal.show();
        
        // Send the line to the terminal
        terminal.sendText(lineText,false);
        // Wait again and send Enter
        setTimeout(() => {
            terminal.sendText('\r', false);
        }, 100);
    });

    context.subscriptions.push(runScene, checkpointPaste, recordedCheckpointPaste, skippedCheckpointPaste, exit, runCurrentLine);
}

function sendCheckpointPaste(argStr = '') {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const selection = editor.selection;
    const text = editor.document.getText(selection);
    
    if (text) {
         // Copy to clipboard
        vscode.env.clipboard.writeText(text);
        // vscode.window.showErrorMessage('No text selected');
        // return;
    } else if (!vscode.env.clipboard.readText()) {
        vscode.window.showErrorMessage('No text selected');
        return;
    }
    
    // Copy to clipboard
    // vscode.env.clipboard.writeText(text);
    
    // Determine if the first line starts with a comment
    const lines = text.split('\n');
    const firstLine = lines[0].trim();
    const startsWithComment = firstLine.startsWith('#');
    
    let command;
    if (lines.length === 1 && !startsWithComment) {
        command = text;
    } else {
        const comment = startsWithComment ? firstLine : '#';
        command = `checkpoint_paste(${argStr}) ${comment} (${lines.length} lines)`;
    }
    
    // Send to terminal
    let terminal = vscode.window.terminals.find(t => t.name === 'Manim');
    if (terminal) {
       // First clear any existing input
        // terminal.sendText('\u0003', false); // Send Ctrl+C
        terminal.show();
        terminal.sendText(command, false);
        
            // Wait again and send Enter
            setTimeout(() => {
                terminal.sendText('\r', false);
            }, 100);
        

    } else {
        vscode.window.showErrorMessage('Manim terminal not found. Run a scene first.');
    }
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};