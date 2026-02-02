chrome.action.onClicked.addListener(() => {
  chrome.tabCapture.capture({ audio: true, video: false }, stream => {
    const ctx = new AudioContext({ sampleRate: 16000 });
    const source = ctx.createMediaStreamSource(stream);
    const processor = ctx.createScriptProcessor(4096, 1, 1);

    const ws = new WebSocket("ws://127.0.0.1:8000/browser-audio");

    source.connect(processor);
    processor.connect(ctx.destination);

    processor.onaudioprocess = e => {
      const data = e.inputBuffer.getChannelData(0);
      ws.send(data.buffer);
    };
  });
});
