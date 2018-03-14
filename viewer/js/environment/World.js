class World
{
  constructor(environmentJson)
  {
    this.x_limit = environmentJson.x_limit;
    this.y_limit = environmentJson.y_limit;
    this.width  = this.x_limit * 2;
    this.height = this.y_limit * 2;
    this.hub    = new Hub(environmentJson);
    this.sites       = [];
    this.obstacles   = [];
    this.traps       = [];
    this.rough       = [];
    this.attractors  = [];
    this.repulsors   = [];
    this.agents      = [];
    this.dead_agents = [];
    this.pheromones  = [];
    this.environment = environmentJson;
    this.test =true;
    this.time=1000;
    this.swarmState = [];
    //this.stateBubbles = new StateBubbles(this);
    //console.log(environmentJson);

    for (let site       of environmentJson.sites      ) { this.sites      .push( new Site      (site      ) ); }
    for (let obstacle   of environmentJson.obstacles  ) { this.obstacles  .push( new Obstacle  (obstacle  ) ); }
    for (let trap       of environmentJson.traps      ) { this.traps      .push( new Trap      (trap      ) ); }
    for (let rough      of environmentJson.rough      ) { this.rough      .push( new Rough     (rough     ) ); }
    for (let attractor  of environmentJson.attractors ) { this.attractors .push( new Attractor (attractor ) ); }
    for (let repulsor   of environmentJson.repulsors  ) { this.repulsors  .push( new Repulsor  (repulsor  ) ); }
    for (let agent      of environmentJson.agents     ) { this.agents     .push( new Agent     (agent     ) ); }
    for (let dead_agent of environmentJson.dead_agents) { this.dead_agents.push( new DeadAgent (dead_agent) ); }
    //for (var pheromone of environmentJson.pheromones)   { this.pheromones .push( new Pheromone (pheromone)  ); }
    this.swarmState.push(new SwarmState(JSON.parse('{"state": "Exploring"}')));
    this.swarmState.push(new SwarmState(JSON.parse('{"state": "Observing"}')));
    this.swarmState.push(new SwarmState(JSON.parse('{"state": "Following site"}')));

  }

  canvasToWorldCoords(x, y)
  {

    return {x: (x - this.x_limit), y: -(y - this.y_limit)};
  }

  update(environment){

    this.pheromones.splice(0,this.pheromones.length)
    this.pheromones=environment.pheromones



	  for (let i = 0; i < this.sites.length; i++) {
		  this.sites[i].x = environment.sites[i].x;
		  this.sites[i].y = -environment.sites[i]["y"];
	  }
	  for (let i = 0; i < this.dead_agents.length; i++) {

		  this.dead_agents[i].x = environment.dead_agents[i].x;
		  this.dead_agents[i].y = -environment.dead_agents[i].y;
	  }
	  //Update Alive Agents
	  for (let i = 0; i < this.agents.length - this.dead_agents.length; i++) {

		  this.agents[i].x = environment.agents[i].x;
		  this.agents[i].y = -environment.agents[i].y;
		  this.agents[i].rotation = Math.PI/2 - environment.agents[i].direction;
      this.agents[i].state = environment.agents[i].state;
	  }


  }
  // Draw the whole world recursively. Takes a 2dRenderingContext obj from
  // a canvas element
  draw(ctx, debug = false, showAgentStates = false, environment)
  {
    let sliderVal = document.getElementById('myRange').value;

    // Ok so this isn't really buying us all that much simplification at this level
    // right *now*, but the point is if in the future we ever need some sort of
    // this drawn singly at a world level, it could go right here very nicely.
    // ctx.shadowColor = 'rgba(51,51,51,.6)';
    // ctx.shadowOffsetX = sliderVal/10;
    // ctx.shadowBlur = 10;
    //path.draw(ctx,this.environment);

//<<<<<<< HEAD

    //TODO: Find the place where the info stations are drawn
    for (var site       of this.sites      ) { site      .draw(ctx, debug); }
    for (var obstacle   of this.obstacles  ) { obstacle  .draw(ctx, debug); }
    for (var trap       of this.traps      ) { trap      .draw(ctx, debug); }
    for (var rough      of this.rough      ) { rough     .draw(ctx, debug); }
    for (var attractor  of this.attractors ) { attractor .draw(ctx, debug); }
    for (var repulsor   of this.repulsors  ) { repulsor  .draw(ctx, debug); }
    //this.pheromones.draw(ctx, debug);
    this.hub.draw(ctx, debug, this.agents);
    //for (var pheromone  of this.pheromones ) { pheromone.draw(ctx,debug)}
    for (var agent      of this.agents     ) { agent     .draw(ctx, debug, showAgentStates,this.hub); }
    for (var dead_agent of this.dead_agents) { dead_agent.draw(ctx, debug); }
    for (var fog        of fogBlock        ) { fog       .checkAgent(this.agents,this.hub); }
    if(showFog){
      for (var fog        of fogBlock        ) { fog       .draw(ctx); }

    }
    for (let state      of this.swarmState ) { state.draw(ctx, this.agents); }
    if(debug ){
      for(let pheromone of this.pheromones){
        ctx.beginPath()

        let x=255//(255-(pheromone.site*(255/this.sites.length))).toString();
        if(x <=0){
          x=0;
        }


        ctx.fillStyle = "rgb("+x.toString()+","+x.toString()+","+x.toString()+")";

        //for (let pheromone of this.pheromones)
        //{
        //console.log(this.pheromones);
        if(pheromone.strength <=0){
          ctx.globalAlpha = .00001

        }else{
          ctx.globalAlpha = (pheromone.strength)*.8

        }
        ctx.beginPath()
        ctx.arc(pheromone.x, -pheromone.y, pheromone.r,0,Math.PI*2);
        //}
        ctx.fill();
        ctx.globalAlpha = 1

      }
    }
//>>>>>>> 0039f9a7c85313d08902ab5a03211a77db5832b0


  }
}
