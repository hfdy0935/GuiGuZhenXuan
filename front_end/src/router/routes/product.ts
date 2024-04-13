export default [
  {
    name: "product",
    path: "/product",
    component: () => import("@/layout/index.vue"),
    redirect: "/product/trademark",
    meta: {
      title: "商品管理",
      hidden: false,
      icon: "Goods",
    },
    children: [
      {
        name: "trademark",
        path: "/product/trademark",
        component: () => import("@/views/Product/TradeMark/index.vue"),
        meta: {
          title: "品牌管理",
          hidden: false,
          icon: "ShoppingCart",
        },
      },
      {
        name: "attr",
        path: "/product/attr",
        component: () => import("@/views/Product/Attr/index.vue"),
        meta: {
          title: "属性管理",
          hidden: false,
          icon: "ChromeFilled",
        },
      },
      {
        name: "spu",
        path: "/product/spu",
        component: () => import("@/views/Product/Spu/index.vue"),
        meta: {
          title: "SPU管理",
          hidden: false,
          icon: "Calendar",
        },
      },
      {
        name: "sku",
        path: "/product/sku",
        component: () => import("@/views/Product/Sku/index.vue"),
        meta: {
          title: "SKU管理",
          hidden: false,
          icon: "Orange",
        },
      },
    ],
  },
];
