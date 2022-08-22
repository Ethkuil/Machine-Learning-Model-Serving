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
    path: '/services',
    name: 'services',
    component: () => import('@/views/Service'),
    meta: { title: '服务' }
  },
  {
    path: '/services/:id',
    name: 'serviceDetail',
    component: () => import('@/views/ServiceDetail'),
    meta: { title: '服务详情' }
  },
  {
    path: '/jobs',
    name: 'jobs',
    component: () => import('@/views/Job'),
    meta: { title: '任务' }
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