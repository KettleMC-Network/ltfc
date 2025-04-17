

events.register<crafttweaker.forge.api.event.block.BlockBreakEvent>(event => {
    if (event.state == <blockstate:minecraft:dirt>) {
		event.setDeny();
		event.level.destroyBlock(event.pos, false, event.player);
	}
});