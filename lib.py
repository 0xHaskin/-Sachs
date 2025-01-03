// src/main.rs
mod agents;
mod models;
mod utils;
mod rig;
mod executor;

use agents::vanguards::vanguards;
use rig::RigFramework;
use executor::Executor;

#[tokio::main]
async fn main() {
    let rig = RigFramework::new();
    let vanguards = vanguards::new(&rig);
    let executor = Executor::new(vanguards);
    
    println!("Goldman vanguards AI Agent Framework initialized.");
    executor.run().await;
}

// src/rig/mod.rs
pub mod core;
pub mod components;

use self::core::RigCore;
use self::components::ComponentManager;

pub struct RigFramework {
    core: RigCore,
    component_manager: ComponentManager,
}

impl RigFramework {
    pub fn new() -> Self {
        Self {
            core: RigCore::new(),
            component_manager: ComponentManager::new(),
        }
    }

    pub fn register_component<T: 'static>(&mut self, component: T) {
        self.component_manager.register(component);
    }
}

// src/rig/core.rs
pub struct RigCore {
    // Core functionality of the rig framework
}

impl RigCore {
    pub fn new() -> Self {
        Self {}
    }
}

// src/rig/components.rs
use std::any::{Any, TypeId};
use std::collections::HashMap;

pub struct ComponentManager {
    components: HashMap<TypeId, Box<dyn Any>>,
}

impl ComponentManager {
    pub fn new() -> Self {
        Self {
            components: HashMap::new(),
        }
    }

    pub fn register<T: 'static>(&mut self, component: T) {
        self.components.insert(TypeId::of::<T>(), Box::new(component));
    }

    pub fn get<T: 'static>(&self) -> Option<&T> {
        self.components.get(&TypeId::of::<T>())
            .and_then(|boxed| boxed.downcast_ref())
    }
}

// src/agents/mod.rs
pub mod agent;
pub mod vanguards;
pub mod researcher;
pub mod writer;

// src/agents/agent.rs
use async_trait::async_trait;
use crate::models::ApiError;
use crate::rig::RigFramework;

#[async_trait]
pub trait Agent {
    fn name(&self) -> String;
    async fn prompt(&self, input: &str) -> Result<String, ApiError>;
    fn initialize(&mut self, rig: &RigFramework);
}

// src/agents/vanguards.rs
use super::agent::Agent;
use async_trait::async_trait;
use crate::models::ApiError;
use crate::rig::RigFramework;

pub struct vanguards {
    rig: Option<RigFramework>,
}

impl vanguards {
    pub fn new(rig: &RigFramework) -> Self {
        let mut vanguards = Self { rig: None };
        vanguards.initialize(rig);
        vanguards
    }
}

#[async_trait]
impl Agent for vanguards {
    fn name(&self) -> String {
        "$vanguards".to_string()
    }

    async fn prompt(&self, input: &str) -> Result<String, ApiError> {
        // Implementation for $vanguards agent
        Ok("$vanguards response".to_string())
    }

    fn initialize(&mut self, rig: &RigFramework) {
        self.rig = Some(rig.clone());
    }
}

// src/executor.rs
use crate::agents::agent::Agent;

pub struct Executor<T: Agent> {
    agent: T,
}

impl<T: Agent> Executor<T> {
    pub fn new(agent: T) -> Self {
        Self
