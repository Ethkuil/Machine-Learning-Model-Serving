import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const routes = [
  {
    path: '/home',
    redirect: '/'
  },
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home'),
    meta: { title: '首页' }
  },
  {
    path: '/deploys',
    component: () => import('@/views/Deploy'),
    name: 'deploys',
    meta: { title: '部署' }
  },
  {
    path: '/deploys/:id',
    name: 'deployDetail',
    component: () => import('@/views/DeployDetail'),
    meta: { title: '部署详情' }
  },
  {
    path: '/models',
    name: 'models',
    component: () => import('@/views/Model'),
    meta: { title: '模型' },
  },
  {
    path: '/models/:id',
    name: 'modelDetail',
    component: () => import('@/views/ModelDetail'),
    meta: { title: '模型详情' }
  },
  {
    path: '/datasets',
    name: 'datasets',
    component: () => import('@/views/Dataset'),
    meta: { title: '数据集' }
  },
]
const router = new Router({
  routes,
  mode: 'history'
})
router.beforeEach((to, from, next) => {
  // 路由发生变化时修改页面title
  if (to.meta && to.meta.title) {
    document.title = to.meta.title
  }
  next()
})
export default router