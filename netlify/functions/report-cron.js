const fetch = require('node-fetch');

exports.handler = async function(event) {
  const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
  const RESEND_API_KEY = process.env.RESEND_API_KEY;
  const REPORT_EMAIL = process.env.REPORT_EMAIL;

  if (!ANTHROPIC_API_KEY || !RESEND_API_KEY || !REPORT_EMAIL) {
    console.error('Missing environment variables');
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
          content: `あなたは親しみやすい株式アナリストです。今夜の投資家向け「予習レポート」を口語体で書いてください。1. 📰 今日の主要ニュース（日本・米国・世界）2. 🇯🇵 東京市場の今日の動き 3. 🇺🇸 今夜のNY市場の注目ポイント 4. 🌍 各国注目ニュース 5. ⚡ 明日の東京市場への影響予測 6. 💡 今夜チェックしておきたい3つのこと。友達に話しかけるような口語体で。最後に「今夜もがんばろう！📈」で締めてください。`
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

    const dateStr = new Date().toLocaleDateString('ja-JP', { timeZone: 'Asia/Tokyo' });

    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${RESEND_API_KEY}`
      },
      body: JSON.stringify({
        from: 'onboarding@resend.dev',
        to: REPORT_EMAIL,
        subject: `🌙【今夜の予習レポート】${dateStr}`,
        text: reportText
      })
    });

    return { statusCode: 200, body: 'Evening report sent' };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
