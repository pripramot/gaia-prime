/**
 * GAIA PRIME - Shared Type Definitions
 *
 * Core types used across the PRIAM monorepo.
 */

/** Agent status in the PRIAM orchestrator */
export type AgentStatus = 'online' | 'offline' | 'standby' | 'error';

/** Tactical sub-system identifiers */
export type SubSystemId =
  | 'phuphadang'
  | 'chronos'
  | 'unicorn'
  | 'gtsalpha-wallet'
  | 'ms-mcp-flutter';

/** Base agent registration info */
export interface AgentInfo {
  id: string;
  name: string;
  subSystem: SubSystemId;
  status: AgentStatus;
  version: string;
  lastHeartbeat: string; // ISO 8601
}

/** MCP message envelope */
export interface McpMessage {
  id: string;
  source: SubSystemId;
  target: SubSystemId | 'orchestrator';
  timestamp: string; // ISO 8601
  payload: unknown;
}

/** Geo-coordinate for CHRONOS tracking */
export interface GeoCoordinate {
  latitude: number;
  longitude: number;
  altitude?: number;
  accuracy?: number;
}

/** CHRONOS tracking point */
export interface TrackingPoint {
  id: string;
  coordinate: GeoCoordinate;
  timestamp: string; // ISO 8601
  deviceId: string;
  metadata?: Record<string, unknown>;
}
