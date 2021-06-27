import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

// TODO: type of Component and props
// const Loadable = (Component: any) => (props: any) => {
//   template: `
//     <Suspense>
//       <template #default>
//         <Component {...${props}} />
//       </template>
//       <template #fallback>
//         <div>Loading ...</div>
//       </template>
//     </Suspense>
//   `;
// };

// const About = Loadable(() => import("../views/About.vue"));
// const Member = Loadable(() => import("../views/Member.vue"));
// const Color = Loadable(() => import("../views/tests/Color.vue"));

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../views/About.vue")
  },
  {
    path: "/member",
    name: "Member",
    component: () => import("../views/Member.vue")
  },
  {
    path: "color",
    name: "Color",
    component: () => import("../views/tests/Color.vue")
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
