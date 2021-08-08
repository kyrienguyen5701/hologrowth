import { ChangeColor } from "@/assets/ts/colors";
import { GetTalentName } from "@/assets/ts/common";
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
    path: "/member/:talentName",
    name: "Member",
    component: () => import("../views/Member.vue"),
    props: true
  },
  {
    path: "color",
    name: "Color",
    component: () => import("../views/tests/Color.vue")
  }
];

const router = new VueRouter({
  // mode: "history",
  // base: process.env.BASE_URL,
  routes
});

router.afterEach((to, from) => {
  const _ = to.params.talentName?.split("-");
  if (_ == undefined) return;
  const talentName = _[_.length - 1];
  ChangeColor(talentName);
})

export default router;
