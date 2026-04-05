/**
 * GAIA PRIME - MCP Core
 *
 * Model Context Protocol core library for inter-agent communication.
 * Provides message creation, routing, and state management primitives
 * for the PRIAM orchestrator.
 */

import type { McpMessage, SubSystemId } from '@gaia-prime/shared-types';
import { generateId, nowISO } from '@gaia-prime/shared-utils';

/**
 * Create a new MCP message envelope.
 */
export function createMcpMessage(
  source: SubSystemId,
  target: SubSystemId | 'orchestrator',
  payload: unknown
): McpMessage {
  return {
    id: generateId(),
    source,
    target,
    timestamp: nowISO(),
    payload,
  };
}

/**
 * Validate the structure of an MCP message.
 */
export function isValidMcpMessage(msg: unknown): msg is McpMessage {
  if (typeof msg !== 'object' || msg === null) return false;
  const m = msg as Record<string, unknown>;
  return (
    typeof m['id'] === 'string' &&
    typeof m['source'] === 'string' &&
    typeof m['target'] === 'string' &&
    typeof m['timestamp'] === 'string' &&
    'payload' in m
  );
}

/** Re-export core types for convenience */
export type { McpMessage, SubSystemId } from '@gaia-prime/shared-types';
