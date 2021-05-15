db.unicorns.find({
vampires: {$exists: false}}).forEach(function (doc) {
printjson(doc);
})

