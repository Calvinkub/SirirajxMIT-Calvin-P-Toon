# Heartstep demo on Vercel

Live: https://heartstep-demo-chi.vercel.app (agent flow) · https://heartstep-demo-chi.vercel.app/problem (problem story) · add `#gif` for the white recording view.

Built from `demo/agent-flow-demo.html` and `demo/problem-story.html`. Redeploy after editing the demo:

```sh
# rebuild index.html from the demo, then
cd deploy/heartstep-demo && vercel deploy --prod --yes
```

Scripted demo, synthetic data, not medical advice.

## Patient app (suteekarn's mobile flow) on Vercel

Live: https://heartstep-app.vercel.app (static, local-storage fallback; no IRIS backend). Source is the repo root (`index.html`, `app.js`, `access.js`, `safety.js`, `runtime.js`, `styles.css`) plus `demo/agent-flow-demo.html` for the trace panel. Copy those into `deploy/heartstep-app/` and run `vercel deploy --prod --yes` there.
