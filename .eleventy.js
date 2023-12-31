module.exports = function(eleventyConfig) {
  const { DateTime } = require("luxon");
  
  eleventyConfig.addPassthroughCopy("css");
  eleventyConfig.addPassthroughCopy("image");
  eleventyConfig.addPassthroughCopy("tumblr_files");

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

