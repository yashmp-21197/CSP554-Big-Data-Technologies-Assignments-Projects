db.unicorns.find({}, {name: 1}).forEach(function (doc) { 
printjson(doc);
})

