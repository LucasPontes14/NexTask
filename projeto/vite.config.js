import { defineConfig } from 'vite'
import { resolve } from 'node:path'

export default defineConfig({
  base: process.env.FIGMA_PUBLIC_URL ? `${process.env.FIGMA_PUBLIC_URL}/` : '/',
  build: {
    rollupOptions: {
      input: {
        inicio: resolve(process.cwd(), 'index.html'),
        sobre: resolve(process.cwd(), 'sobre.html'),
        acervo: resolve(process.cwd(), 'acervo.html'),
        periodos: resolve(process.cwd(), 'periodos.html'),
        lugares: resolve(process.cwd(), 'lugares.html'),
        pesquisadores: resolve(process.cwd(), 'pesquisadores.html'),
        visitas: resolve(process.cwd(), 'visitas.html'),
        contato: resolve(process.cwd(), 'contato.html'),
        mercado: resolve(process.cwd(), 'mercado-publico.html'),
        biblioteca: resolve(process.cwd(), 'biblioteca-municipal.html'),
        museu: resolve(process.cwd(), 'museu-nilo-pereira.html'),
        estacao: resolve(process.cwd(), 'estacao-ferroviaria.html'),
        login: resolve(process.cwd(), 'login.html'),
      },
    },
  },
  server: {
    host: process.env.FIGMA_DEV_SERVER_HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '8443'),
    strictPort: true,
  },
  preview: {
    host: process.env.FIGMA_DEV_SERVER_HOST || '0.0.0.0',
    port: parseInt(process.env.PORT || '8443'),
  },
})
