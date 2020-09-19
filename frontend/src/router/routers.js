import Main from '@/components/main'
import parentView from '@/components/parent-view'

/**
 * iview-admin中meta除了原生参数外可配置的参数:
 * meta: {
 *  title: { String|Number|Function }
 *         显示在侧边栏、面包屑和标签栏的文字
 *         使用'{{ 多语言字段 }}'形式结合多语言使用，例子看多语言的路由配置;
 *         可以传入一个回调函数，参数是当前路由对象，例子看动态路由和带参路由
 *  hideInBread: (false) 设为true后此级路由将不会出现在面包屑中，示例看QQ群路由配置
 *  hideInMenu: (false) 设为true后在左侧菜单不会显示该页面选项
 *  notCache: (false) 设为true后页面在切换标签后不会缓存，如果需要缓存，无需设置这个字段，而且需要设置页面组件name属性和路由配置的name一致
 *  access: (null) 可访问该页面的权限数组，当前路由设置的权限会影响子路由
 *  icon: (-) 该页面在左侧菜单、面包屑和标签导航处显示的图标，如果是自定义图标，需要在图标名称前加下划线'_'
 *  beforeCloseName: (-) 设置该字段，则在关闭当前tab页时会去'@/router/before-close.js'里寻找该字段名对应的方法，作为关闭前的钩子函数
 * }
 */

export default [
  {
    path: '/login',
    name: 'login',
    meta: {
      title: 'Login - 登录',
      hideInMenu: true
    },
    component: () => import('@/view/login/login.vue')
  },
  {
    path: '/',
    name: '_home',
    redirect: '/home',
    component: Main,
    meta: {
      //hideInMenu: true,
      notCache: true
    },
    children: [
      {
        path: '/home',
        name: 'home',
        meta: {
          //hideInMenu: true,
          title: '首页',
          notCache: true,
          icon: 'md-home'
        },
        component: () => import('@/view/single-page/home')
      }
    ]
  },
  {
    path: '/category',
    name: 'category',
    meta: {
      icon: 'md-cloud-upload',
      title: 'category'
    },
    component: Main,
    children: [
      {
        path: 'data_center',
        name: 'data_center',
        meta: {
          icon: 'md-podium',
          title: 'data_center',
          showAlways: true
        },
        component: parentView,
        children: [
          {
            path: 'idcs',
            name: 'idcs',
            meta: {
              icon: 'ios-home',
              title: 'idcs'
            },
            component: () => import('@/view/projects/category/idcs.vue')
          },
          {
            path: '/category/idcs/:id',
            name: 'idc_detail',
            meta: {
              hideInMenu: true,
              icon: 'ios-document',
              title: 'idc_detail'
            },
            component: () => import('@/view/projects/category/idc_detail.vue')
          },
          {
            path: 'racks',
            name: 'racks',
            meta: {
              icon: 'ios-cart',
              title: 'racks'
            },
            component: () => import('@/view/projects/category/racks.vue')
          },
          {
            path: '/category/racks/:id',
            name: 'rack_detail',
            meta: {
              hideInMenu: true,
              icon: 'ios-document',
              title: 'rack_detail'
            },
            component: () => import('@/view/projects/category/rack_detail.vue')
          },
          {
            path: 'servers',
            name: 'servers',
            meta: {
              icon: 'logo-tux',
              title: 'servers'
            },
            component: () => import('@/view/projects/category/servers.vue')
          },
          {
            path: '/category/servers/:id',
            name: 'server_detail',
            meta: {
              hideInMenu: true,
              icon: 'ios-document',
              title: 'server_detail'
            },
            component: () => import('@/view/projects/category/server_detail.vue')
          },
          {
            path: 'sshusers',
            name: 'sshusers',
            meta: {
              icon: 'ios-person',
              title: 'sshusers'
            },
            component: () => import('@/view/projects/category/sshusers.vue')
          }

        ]
      },
      {
        path: 'business_info',
        name: 'business_info',
        meta: {
          icon: 'ios-globe',
          title: 'business_info',
          showAlways: true
        },
        component: parentView,
        children: [
          {
            path: 'businesslines',
            name: 'businesslines',
            meta: {
              icon: 'ios-git-network',
              title: 'businesslines'
            },
            component: () => import('@/view/projects/category/businesslines.vue')
          },
          {
            path: 'projects',
            name: 'projects',
            meta: {
              icon: 'ios-cube',
              title: 'projects'
            },
            component: () => import('@/view/projects/category/projects.vue')
          },
          {
            path: '/category/projects/:id',
            name: 'project_detail',
            meta: {
              hideInMenu: true,
              icon: 'ios-document',
              title: 'project_detail'
            },
            component: () => import('@/view/projects/category/project_detail.vue')
          },
          {
            path: '/category/webssh/:server_id/:user_id',
            name: 'webssh_detail',
            meta: {
              hideInMenu: true,
              icon: 'ios-document',
              title: 'webssh_detail'
            },
            component: () => import('@/view/projects/category/webssh_detail.vue')
          },

        ]
      }

    ]
  },

  {
    path: '/account',
    name: 'account',
    meta: {
      icon: 'md-person',
      title: 'account'
    },
    component: Main,
    children: [
      {
        path: 'users',
        name: 'users',
        meta: {
          icon: 'ios-person',
          title: 'users'
        },
        component: () => import('@/view/projects/account/users.vue')
      },
      {
        path: 'groups',
        name: 'groups',
        meta: {
          icon: 'ios-people',
          title: 'groups'
        },
        component: () => import('@/view/projects/account/groups.vue')
      }
    ]
  },

  {
    path: '/history',
    name: 'history',
    meta: {
      icon: 'md-person',
      title: 'history'
    },
    component: Main,
    children: [
      {
        path: 'histories',
        name: 'histories',
        meta: {
          icon: 'ios-person',
          title: 'histories'
        },
        component: () => import('@/view/projects/history/histories.vue')
      },
      {
        path: '/history/histories/:id',
        name: 'history_detail',
        meta: {
          hideInMenu: true,
          icon: 'ios-document',
          title: 'history_detail'
        },
        component: () => import('@/view/projects/history/history_detail.vue')
      },

    ]
  },

]
