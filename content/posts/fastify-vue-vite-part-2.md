---
title: "Adding Vue Router and Shadcn-Vue to Fastify and Vite: Part 2"
date: 2024-11-12  T10:44:27-04:00
draft: false
description: "Continuing the setup by adding Vue Router for page navigation and integrating Shadcn-Vue for building modern UIs."
tags: ["javascript","vue","nodejs"]
author: "Me"
categories: ["Tech"]
series: ["Build with Me"]
---

In Part 1, I walked through setting up Fastify, Vite, and TypeScript together, including all the gotchas I ran into along the way. Now that the backend and front-end tooling are working smoothly, it's time to take things up a notch by adding page routing with Vue Router and enhancing the UI with Shadcn-Vue.

## Adding Vue Router

The first step to building a more dynamic front-end is introducing client-side routing. This will let us navigate between different pages without needing full page reloads—a must-have for any modern web application. Vue Router is the standard tool for this job when working with Vue.

### Step 1: Install Vue Router
To get started, you’ll need to install Vue Router:

```bash
pnpm add vue-router
```

### Step 2: Create a Router File
Now that Vue Router is installed, let’s create a file called `router.ts` inside the `src/frontend/` directory to set up our routes.

```typescript
import { createRouter, createWebHistory } from 'vue-router';
import Home from './pages/Home.vue';
import About from './pages/About.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
```

This configuration sets up two basic routes: a home page (`/`) and an about page (`/about`). You can easily extend this to include more pages as your app grows.

### Step 3: Integrate the Router with `App.vue`
Now let’s integrate Vue Router into our main application component. First, create an `App.vue` file in `src/frontend/` if you haven’t already.

```vue
<template>
  <router-view />
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});
</script>

<style scoped>
/* Add any general styles for the application here */
</style>
```

The `<router-view />` component is where the routed components (like `Home.vue` and `About.vue`) will be displayed.

### Step 4: Update `main.ts`
Next, update the `main.ts` file to use Vue Router:

```typescript
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

createApp(App)
  .use(router)
  .mount('#app');
```

This sets up the router and mounts it within the Vue app. Now, you can navigate between the `Home` and `About` pages without reloading the browser.

## Adding Shadcn-Vue for UI Components

To add shadcn, I'm mostly drawing off their great installation instructions [here](https://www.shadcn-vue.com/docs/installation/vite.html). But in summary:

### Step 1: Make sure Tailwind CSS is installed and compiling with `postcss`

In specific, I had to update my `vite.config` to match the instructions:

```typescript
import { fileURLToPath, URL } from 'node:url'

import autoprefixer from 'autoprefixer'
import tailwind from 'tailwindcss'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
css: {
    postcss: {
    plugins: [tailwind(), autoprefixer()],
    },
},
plugins: [
    vue(),
],
resolve: {
    alias: {
    '@': fileURLToPath(new URL('./src', import.meta.url))
    }
}
})
```
### Step 2. Edit your `tsconfig`

Again, I'm just matching what's in the instructions:

```json
{
  "compilerOptions": {
    // ...
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
    // ...
  }
}
```
The instructions recommend deleting the `.src/style.css` next. 

### Step 3. Run the CLI

The big step is to run the CLI, which will configure everything else:

    npx shadcn-vue@latest init

### Step 4. Update `main.ts`

Finally, you'll need to swap out your original tailwind.css for the compiled shadcn version:

```typesccript
import { createApp } from 'vue'
- import './tailwind.css'
import App from './App.vue'
+ import './assets/index.css'

createApp(App).mount('#app')
```

This makes building a cohesive and visually appealing interface quick and simple.

## Conclusion
In Part 2, we added Vue Router to enable seamless page navigation and Shadcn-Vue to enhance our UI with modern, reusable components. With these tools in place, our Fastify + Vite stack is well on its way to being a dynamic and visually appealing full-stack application.

I've put all the code up until this up on my [GitHub](https://github.com/jgennari/fastify-vite-ts).