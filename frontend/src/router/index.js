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
    path: '/deploy',
    name: 'deploy',
    component: () => import('@/views/Deploy'),
    meta: { title: '部署' }
  },
  {
    path: '/model',
    name: 'model',
    component: () => import('@/views/Model'),
    meta: { title: '模型' }
  }
  // {
  //   path: '/deploy/:id',
  //   name: 'deploy-detail',
  //   component: () => import('@/views/DeployDetail'),
  //   meta: { title: '部署详情' }
  // },
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