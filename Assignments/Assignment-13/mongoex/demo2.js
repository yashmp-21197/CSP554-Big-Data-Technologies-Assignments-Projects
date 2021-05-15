db.unicorns.find({gender: 'm',
weight: {$gt: 700}}).forEach(function(doc) {
    printjson(doc);
})

