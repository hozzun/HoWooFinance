import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ArticlesView from '@/views/ArticlesView.vue'
import CloseBankView from '@/views/CloseBankView.vue'
import ExchangeRateView from '@/views/ExchangeRateView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import MyLikesView from '@/views/MyLikesView.vue'
import MyPageView from '@/views/MyPageView.vue'
import CreateView from '@/views/CreateView.vue'
import ArticlesDetailView from '@/views/ArticlesDetailView.vue'
import Deposits from '@/components/Deposits.vue'
import MyRecommends from '@/components/MyRecommends.vue'
import Savings from '@/components/Savings.vue'
import ProductList from '@/components/ProductList.vue'
import ProductDetail from '@/components/ProductDetail.vue'
import ArticlesUpdateView from '@/views/ArticlesUpdateView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView
    },
    {
      path: '/mylikes',
      name: 'mylikes',
      component: MyLikesView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/productlist',
      name: 'productlist',
      component: ProductList
    },
    {
      path: '/products/:fin_prdt_cd/:type',
      name: 'productdetail',
      component: ProductDetail,
      props: true
    },
    {
      path: '/exchange_rate',
      name: 'exchangerate',
      component: ExchangeRateView
    },
    {
      path: '/close_bank',
      name: 'closebank',
      component: CloseBankView
    },
    {
      path: '/articles',
      name: 'articles',
      component: ArticlesView
    },
    {
      path: '/deposits',
      name: 'deposits',
      component: Deposits
    },
    {
      path: '/savings',
      name: 'savings',
      component: Savings
    },
    {
      path: '/myrecommends',
      name: 'myrecommends',
      component: MyRecommends
    },
    {
      path: '/create',
      name: 'create',
      component: CreateView
    },
    {
      path: '/articles/:id',
      name: 'articlesdetail',
      component: ArticlesDetailView
    },
    {
      path: '/articles/:id/update',
      name: 'articlesupdate',
      component: ArticlesUpdateView,
    },
  ]
})

export default router