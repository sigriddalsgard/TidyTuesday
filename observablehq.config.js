// See https://observablehq.com/framework/config for documentation.
export default {
  // The project’s title; used in the sidebar and webpage titles.
  title: "Sigrid",

  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  pages: [
    {
      name: "Tidy Tuesday 2024",
      collapsible: true,
      pages: [
        {name: "Week 17", path: "/2024/week-17/"},
        {name: "Week 18", path: "/2024/week-18/"},
        {name: "Week 19", path: "/2024/week-19/"},
        {name: "Week 20", path: "/2024/week-20/"},
        {name: "Week 21", path: "/2024/week-21/"}
      ]
    }
  ],

  // Some additional configuration options and their defaults:
  //theme: "default", // try "light", "dark", "slate", etc.
  // header: "", // what to show in the header (HTML)
  // footer: "Built with Observable.", // what to show in the footer (HTML)
  // toc: true, // whether to show the table of contents
  pager: false, // whether to show previous & next links in the footer
  // root: "docs", // path to the source root for preview
  // output: "dist", // path to the output root for build
  // search: true, // activate search
};
