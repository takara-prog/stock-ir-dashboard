const fetch = require('node-fetch');

exports.handler = async function(event) {
  const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
  const LINE_NOTIFY_TOKEN = process.env.LINE_NOTIFY_TOKEN;

  if (!ANTHROPIC_API_KEY || !LINE_NOTIFY_TOKEN) {
    return { statusCode: 500, body: 'Missing env vars' };
  }

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-5',
        max_tokens: 2000,
        tools: [{ type: 'web_search_20250305', name: 'web_search' }],
        messages: [{
          role: 'user',
          content: `あなたは親しみやすい株式アナリストです。昨夜のNY市場の結果と今朝の東京市場の開幕予測を口語体でまとめてください。1. 🌙 昨夜のNY市場結果（ダウ・S&P500・ナスダック）2. 📊 セクター別パフォーマンス 3. 💬 昨夜の決算発表・主要ニュースの影響 4. 🌍 欧州・アジア市場の動き 5. 🇯🇵 今朝の東京市場 開幕予測 6. 📌 今日の注目銘柄・セクター3つ。「おはよう！昨夜はね〜」から始めて。最後に「今日も良いトレードを！🌅」で締めてください。`
        }]
      })
    });

    const data = await response.json();
    let reportText = '';
    if (data.content) {
      for (const block of data.content) {
        if (block.type === 'text') reportText += block.text;
      }
    }
    if (!reportText) throw new Error('No text content from Claude');

    const header = `\n🌅【昨夜の結果まとめ】\n${new Date().toLocaleDateString('ja-JP', { timeZone: 'Asia/Tokyo' })}\n${'─'.repeat(20)}\n\n`;
    const fullMessage = header + reportText;
    const chunks = [];
    for (let i = 0; i < fullMessage.length; i += 1900) {
      chunks.push(fullMessage.slice(i, i + 1900));
    }

    for (const chunk of chunks) {
      await fetch('https://notify-api.line.me/api/notify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': `Bearer ${LINE_NOTIFY_TOKEN}`
        },
        body: new URLSearchParams({ message: chunk })
      });
      await new Promise(r => setTimeout(r, 500));
    }

    return { statusCode: 200, body: 'Morning report sent' };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
