import styled from 'styled-components';
import { neutral } from '../../constants/colors';

export const Container = styled.div`
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  background: radial-gradient(120% 60% at 20% 10%, #eef2ff 0%, rgba(238, 242, 255, 0) 60%),
    radial-gradient(100% 40% at 80% 0%, #e0f7f1 0%, rgba(224, 247, 241, 0) 60%),
    ${neutral};
`;

export const ChatBody = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 12px 16px;
  box-sizing: border-box;
`;

export const MessagesContainer = styled.div`
  flex: 1;
  padding: 12px 0 12px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 18px;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  box-sizing: border-box;
  scrollbar-width: thin;
  scrollbar-color: #d6d6e7 transparent;

  &::-webkit-scrollbar {
    width: 8px;
  }
  &::-webkit-scrollbar-track {
    background: transparent;
  }
  &::-webkit-scrollbar-thumb {
    background-color: #d6d6e7;
    border-radius: 999px;
  }
`;

export const InputWrapper = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 8px 12px 16px;
  box-sizing: border-box;
  background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.9) 40%, rgba(255,255,255,1) 100%);
  position: sticky;
  bottom: 0;
  left: 0;
  right: 0;
`;
