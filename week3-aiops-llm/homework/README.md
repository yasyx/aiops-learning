- 在项目根目录新建 .env 文件，内容如下
```shell
OPENAI_API_KEY=<you_openai_api_key>
# langchain 可以是代理地址
OPENAI_API_BASE=<you_openai_base_url>
# openAI 原生API 可以是代理地址
OPENAI_BASE_URL=<you_openai_base_url>
```

- 执行如下命令
```python

python week3-aiops-llm/homework/func-call/main.py

```

- 输出如下：

```
    向ChatGPT发送消息：content='帮我修改 gateway 的配置，vendor 修改为 alipay' additional_kwargs={} response_metadata={}
    命中modify_config方法，其参数为：{'service_name': 'gateway', 'key': 'vendor', 'value': 'alipay'},ID为：call_W6ZcV497IXb0zvc7vZrSixoR
    The Function [modify_config] was called!!!
    将tool类型的消息返回至LLM解析，其内容为：[ToolMessage(content='The config of gateway was modified, detail: modify the value of vendor to alipay', name='modify_config', tool_call_id='call_W6ZcV497IXb0zvc7vZrSixoR')]
    ChatGPT返回：已成功将 gateway 的配置中的 vendor 修改为 alipay。
    ================================================================
    向ChatGPT发送消息：content='帮我重启 gateway 服务' additional_kwargs={} response_metadata={}
    命中restart_service方法，其参数为：{'service_name': 'gateway'},ID为：call_QgyuUPHFONes8Twzn8pE76Wq
    The Function [restart_service] was called!!!
    将tool类型的消息返回至LLM解析，其内容为：[ToolMessage(content='The service of gateway was restarted', name='restart_service', tool_call_id='call_QgyuUPHFONes8Twzn8pE76Wq')]
    ChatGPT返回：gateway 服务已成功重启。
    ================================================================
    向ChatGPT发送消息：content='帮我部署一个 deployment，镜像是 nginx' additional_kwargs={} response_metadata={}
    命中apply_manifest方法，其参数为：{'resouce_type': 'deployment', 'image': 'nginx'},ID为：call_L3ObQlXpe64eam9po1PbkGZ3
    The Function [apply_manifest] was called!!!
    将tool类型的消息返回至LLM解析，其内容为：[ToolMessage(content='A new deployment manifest was applied with image: nginx', name='apply_manifest', tool_call_id='call_L3ObQlXpe64eam9po1PbkGZ3')]
    ChatGPT返回：已成功部署一个新的 deployment，镜像为 nginx。
```