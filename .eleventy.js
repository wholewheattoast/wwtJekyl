const pluginRss = require("@11ty/eleventy-plugin-rss");
// consider for update after ver 3
// const { eleventyImageTransformPlugin } = require("@11ty/eleventy-img");
const Image = require("@11ty/eleventy-img");

module.exports = function(eleventyConfig) {
  const { DateTime } = require("luxon");

  eleventyConfig.addPlugin(pluginRss, {
    posthtmlRenderOptions: {
      closingSingleTag: "default" // opt-out of <img/>-style XHTML single tags
    }
  });
  // Only one module.exports per configuration file, please!
  eleventyConfig.addShortcode("image", async function (src, alt, sizes) {
    let metadata = await Image(src, {
      widths: [368, 736, 900],
      formats: ["webp", "jpeg"],
      urlPath: "/image-processed/",
      outputDir: "./image-processed/",
    });

    let imageAttributes = {
      alt,
      sizes,
      loading: "lazy",
      decoding: "async",
    };

    // You bet we throw an error on a missing alt (alt="" works okay)
    return Image.generateHTML(metadata, imageAttributes);
  });

  eleventyConfig.addLiquidFilter("dateToRfc3339", pluginRss.dateToRfc3339);
  eleventyConfig.addLiquidFilter("dateToRfc822", pluginRss.dateToRfc822);

  eleventyConfig.addPassthroughCopy("css");
  eleventyConfig.addPassthroughCopy("image");
  eleventyConfig.addPassthroughCopy("image-processed");
  eleventyConfig.addPassthroughCopy("tumblr_files");
  eleventyConfig.addPassthroughCopy("keybase.txt");
  
  eleventyConfig.addShortcode("year", () => `${new Date().getFullYear()}`);

  eleventyConfig.addFilter("justYear", (dateString) => {
    dateObj = new Date(dateString);
    return DateTime.fromJSDate(dateObj, { zone: 'utc' }).toFormat('yyyy');
  });
  
  eleventyConfig.addFilter("justMonth", (dateString) => {
    dateObj = new Date(dateString);
    return DateTime.fromJSDate(b_dateObj, { zone: 'utc' }).toFormat('MM');
  });
  
  // Display tag list on page
  // copied from 
  eleventyConfig.addCollection('tagsList', function (collectionApi) {
    const tagsList = new Set()
    collectionApi.getAll().map((item) => {
      if (item.data.tags) {
        // handle pages that don't have tags
        item.data.tags.filter((tag) => !['yourtag'].includes(tag)).map((tag) => tagsList.add(tag))
      }
    })
    return tagsList
  })
};
