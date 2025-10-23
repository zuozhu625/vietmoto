const { ChatOpenAI } = require('@langchain/openai');

async function testLangChain() {
  console.log('🧪 测试 LangChain + Gemini 2.5 Flash...');
  
  try {
    const llm = new ChatOpenAI({
      modelName: 'google/gemini-2.0-flash-exp:free',
      temperature: 0.9,
      maxTokens: 500,
      openAIApiKey: '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',
      configuration: {
        baseURL: 'https://openrouter.ai/api/v1',
      },
    });

    console.log('📤 发送测试请求...');
    const result = await llm.invoke('Viết một câu ngắn về xe máy Honda Winner X bằng tiếng Việt (chỉ 1-2 câu)');
    
    console.log('✅ 响应成功:');
    console.log(result.content);
    console.log('\n✨ LangChain工作正常！');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.error('详细错误:', error);
  }
}

testLangChain();

