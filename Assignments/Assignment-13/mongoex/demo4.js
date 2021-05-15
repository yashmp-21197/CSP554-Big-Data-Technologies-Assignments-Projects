db.unicorns.find({
loves: {$in:['apple','orange']}}).forEach(function (doc) {
printjson(doc);
})

