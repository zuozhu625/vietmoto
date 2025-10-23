const http = require('http');

async function generateReviews(count) {
  console.log(`🚀 开始生成 ${count} 条用户测评...`);
  
  for (let i = 1; i <= count; i++) {
    console.log(`\n📝 正在生成第 ${i}/${count} 条测评...`);
    
    try {
      await new Promise((resolve, reject) => {
        const options = {
          hostname: 'localhost',
          port: 4001,
          path: '/api/news',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        };

        const req = http.request(options, (res) => {
          let data = '';
          
          res.on('data', (chunk) => {
            data += chunk;
          });
          
          res.on('end', () => {
            if (res.statusCode === 201 || res.statusCode === 200) {
              console.log(`✅ 第 ${i} 条测评生成成功`);
              resolve();
            } else {
              console.log(`⚠️  第 ${i} 条测评生成返回状态: ${res.statusCode}`);
              resolve(); // 继续生成下一条
            }
          });
        });

        req.on('error', (error) => {
          console.error(`❌ 第 ${i} 条测评生成失败:`, error.message);
          resolve(); // 继续生成下一条
        });

        // 发送触发请求（通过ReviewScheduler生成）
        req.write(JSON.stringify({
          title: '_trigger_review_generation_',
          content: 'trigger',
          summary: 'trigger',
          category: 'trigger',
          status: 'draft'
        }));
        req.end();
      });

      // 等待10秒，避免API频率限制
      if (i < count) {
        console.log('⏳ 等待10秒后生成下一条...');
        await new Promise(resolve => setTimeout(resolve, 10000));
      }
    } catch (error) {
      console.error(`❌ 生成第 ${i} 条时出错:`, error);
    }
  }
  
  console.log('\n🎉 所有测评生成任务完成！');
  console.log('📊 查看生成的测评: http://47.237.79.9:4001/api/news?category=Đánh%20giá%20người%20dùng');
}

// 生成6条测评
generateReviews(6);

