import mods.jeitweaker.Jei;

<recipetype:minecraft:crafting>.remove(<item:waystones:waystone>);


<recipetype:minecraft:crafting>.addShaped("lftc.waystone", <item:waystones:waystone>, [
	[<item:minecraft:air>, <tag:items:tfc:rock/bricks>, <item:minecraft:air>],
	[<tag:items:tfc:rock/bricks>, <item:tfc:gem/amethyst>, <tag:items:tfc:rock/bricks>],
	[<tag:items:forge:ingots/copper>, <tag:items:forge:ingots/copper>, <tag:items:forge:ingots/copper>]
]);



Jei.hideIngredients([
    <item:minecraft:diamond>,
    <item:minecraft:emerald>,
    <item:minecraft:coal>,
    <item:minecraft:netherite_ingot>,
    <item:minecraft:gold_ingot>,
    <item:minecraft:iron_ingot>,
    <item:minecraft:copper_ingot>,
	<item:waystones:mossy_waystone>,
	<item:waystones:sandy_waystone>,
	<item:waystones:warp_plate>,
	<item:waystones:portstone>,
	<item:waystones:warp_stone>,
	<item:waystones:warp_stone>,
	<item:waystones:warp_dust>,
	<item:waystones:return_scroll>,
	<item:waystones:bound_scroll>,
	<item:waystones:warp_scroll>
]);

Jei.hideIngredients(<tag:items:waystones:sharestone>);

for item in loadedMods.minecraft.itemStacks {
	print(item.asIIngredientWithAmount().ingredient.commandString);
}